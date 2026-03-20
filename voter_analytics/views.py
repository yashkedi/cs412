# voter_analytics/views.py
# Yash Kedia (yashkedi@bu.edu), 3/19/26
# Description: Views for voter_analytics application

from django.shortcuts import render
from django.views.generic import ListView, DetailView
import plotly
from collections import Counter
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.colors import qualitative
from django.db.models import Count
from .models import Voter

# Create your views here.
class VotersListView(ListView):
    '''View to display voter results'''
 
    template_name = 'voter_analytics/results.html'
    model = Voter
    context_object_name = 'results'
    paginate_by = 100  # show 100 voters per page to avoid overwhelming the browser

    def get_queryset(self):

        # start with entire queryset, alphabetically sorted
        results = super().get_queryset().order_by('last_name', 'first_name')

        # read optional filter parameters from the GET request
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        #filter results — each block only applies if the user provided that filter
        if party:
            results = results.filter(party__iexact=party.strip())  # case-insensitive match

        if min_dob:
            results = results.filter(dob__year__gte=int(min_dob))  # birth year >= min

        if max_dob:
            results = results.filter(dob__year__lte=int(max_dob))  # birth year <= max

        if voter_score:
            results = results.filter(voter_score=voter_score)  # exact score match

        # dynamically filter by any checked election participation checkboxes
        for field in ['v20', 'v21town', 'v21primary', 'v22', 'v23']:
            if self.request.GET.get(field):
                results = results.filter(**{field: True})  # only keep voters who participated

        return results

    def get_context_data(self, **kwargs):
        '''override the built in get_context_data to populate fields.'''
        context = super().get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        if 'page' in get_copy:
            del get_copy['page']  # drop page param so pagination links don't double-encode it
        context['query_string'] = get_copy.urlencode()  # pass active filters to the template for pagination links
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['years'] = range(1900, 2007)  # birth year range for the filter dropdowns
        context['scores'] = range(0, 6)       # voter_score can be 0–5
        context['get'] = self.request.GET     # expose current GET params so the form can pre-select values
        return context
      
class VoterDetailView(DetailView):
    '''View for handling a single instance of a voter's details.'''
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'
    
class GraphListView(ListView):
    '''View for displaying graphs of voter data.'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        '''Return filtered queryset based on GET parameters.'''
        queryset = Voter.objects.all()

        # read the same filter params as VotersListView
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        if party:
            queryset = queryset.filter(party=party)
        if min_dob:
            queryset = queryset.filter(dob__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(dob__year__lte=int(max_dob))
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # apply election participation filters using dynamic field lookup
        for field in ['v20', 'v21town', 'v21primary', 'v22', 'v23']:
            if self.request.GET.get(field):
                queryset = queryset.filter(**{field: True})

        return queryset

    def get_context_data(self, **kwargs):
        '''Override get_context_data to add graphs and form choices.'''
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()  # re-fetch filtered queryset for graph data

        # populate filter form choices
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['years'] = range(1900, 2007)
        context['scores'] = range(0, 6)
        context['get'] = self.request.GET  # pre-select current filters in the form

        # graph 1: birth year histogram — skip voters with no recorded dob
        years = [v.dob.year for v in voters if v.dob]
        year_counts = Counter(years)  # tally how many voters were born each year
        fig_birth = go.Figure(data=[go.Bar(
            x=list(year_counts.keys()),
            y=list(year_counts.values())
        )])
        fig_birth.update_layout(
            title="Distribution of Voters by Year of Birth",
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters"
        )
        context['graph_birth'] = plotly.offline.plot(fig_birth, auto_open=False, output_type="div")  # embed as HTML div

        # graph 2: party pie chart — fall back to 'Unknown' for voters with no party
        parties = [v.party if v.party else 'Unknown' for v in voters]
        party_counts = Counter(parties)
        fig_party = go.Figure(data=[go.Pie(
            labels=list(party_counts.keys()),
            values=list(party_counts.values()),
            marker=dict(colors=qualitative.Set3)  # use a categorical color palette
        )])
        fig_party.update_layout(title="Distribution of Voters by Party Affiliation")
        context['graph_party'] = plotly.offline.plot(fig_party, auto_open=False, output_type="div")

        # graph 3: election participation bar chart — count voters who turned out per election
        election_fields = ['v20', 'v21town', 'v21primary', 'v22', 'v23']
        participation_counts = {field: 0 for field in election_fields}  # start all counts at 0
        for v in voters:
            for field in election_fields:
                if getattr(v, field):  # True means the voter participated in that election
                    participation_counts[field] += 1
        fig_participation = go.Figure(data=[go.Bar(
            x=list(participation_counts.keys()),
            y=list(participation_counts.values())
        )])
        fig_participation.update_layout(
            title="Voter Participation Across Elections",
            xaxis_title="Election",
            yaxis_title="Number of Voters"
        )
        context['graph_participation'] = plotly.offline.plot(fig_participation, auto_open=False, output_type="div")

        return context