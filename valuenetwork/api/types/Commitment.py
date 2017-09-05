#
# Commitment: A planned economic event or transfer that has been promised by an agent to another agent.
#


import graphene
from graphene_django.types import DjangoObjectType

import valuenetwork.api.types as types
from valuenetwork.api.types.QuantityValue import Unit, QuantityValue
from valuenetwork.valueaccounting.models import Commitment as CommitmentProxy
from valuenetwork.api.models import formatAgent, Person, Organization, QuantityValue as QuantityValueProxy, Fulfillment as FulfillmentProxy


class Commitment(DjangoObjectType):
    action = graphene.String(source='action')
    #process = graphene.Field(lambda: types.Process)
    input_of = graphene.Field(lambda: types.Process)
    output_of = graphene.Field(lambda: types.Process)
    provider = graphene.Field(lambda: types.Agent)
    receiver = graphene.Field(lambda: types.Agent)
    scope = graphene.Field(lambda: types.Agent)
    resource_classified_as = graphene.Field(lambda: types.ResourceClassification)
    involves = graphene.Field(lambda: types.EconomicResource)
    committed_quantity = graphene.Field(QuantityValue)
    committed_on = graphene.String(source='committed_on')
    planned_start = graphene.String(source='planned_start')
    due = graphene.String(source='due')
    is_finished = graphene.Boolean(source='is_finished')
    note = graphene.String(source='note')

    class Meta:
        model = CommitmentProxy
        only_fields = ('id')

    fulfilled_by = graphene.List(lambda: types.Fulfillment)

    involved_agents = graphene.List(lambda: types.Agent)

    #def resolve_process(self, args, *rargs):
    #    return self.process

    def resolve_input_of(self, args, *rargs):
        return self.input_of

    def resolve_output_of(self, args, *rargs):
        return self.output_of

    def resolve_provider(self, args, *rargs):
        return formatAgent(self.provider)

    def resolve_receiver(self, args, *rargs):
        return formatAgent(self.receiver)

    def resolve_scope(self, args, *rargs):
        return formatAgent(self.scope)

    def resolve_involves(self, args, *rargs):
        return self.involves

    def resolve_resource_classified_as(self, args, *rargs):
        return self.resource_classified_as

    def resolve_committed_quantity(self, args, *rargs):
        return QuantityValueProxy(numeric_value=self.quantity, unit=self.unit_of_quantity)

    def resolve_fulfilled_by(self, args, context, info):
        events = self.fulfillment_events.all()
        fulfillments = []
        for event in events:
            fulfill = FulfillmentProxy(
                fulfilled_by=event,
                fulfills=self,
                fulfilled_quantity=QuantityValueProxy(numeric_value=event.quantity, unit=event.unit_of_quantity),
                )
            fulfillments.append(fulfill)
        return fulfillments

    def resolve_involved_agents(self, args, context, info):
        involved = []
        if self.provider:
            involved.append(formatAgent(self.provider))
        events = self.fulfillment_events.all()
        for event in events:
            if event.provider:
                involved.append(formatAgent(event.provider))
        return list(set(involved))
