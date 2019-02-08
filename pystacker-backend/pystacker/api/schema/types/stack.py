from graphql import GraphQLString, GraphQLNonNull, GraphQLList, GraphQLObjectType, GraphQLField, GraphQLInt, GraphQLScalarType

from .service import ServiceType
from ..query.service import resolve_services

ExtraValuesType = GraphQLScalarType(
    name="MetaData",
    serialize=lambda x: x
)

StackType = GraphQLObjectType(
    name="stack",
    fields={
        "id": GraphQLField(GraphQLInt),
        "name": GraphQLField(GraphQLNonNull(GraphQLString)),
        "from_template": GraphQLField(GraphQLNonNull(GraphQLString)),
        "services": GraphQLField(GraphQLList(
                ServiceType,
            ),
            resolve=resolve_services
        ),
        "meta": GraphQLField(ExtraValuesType, resolve=lambda stack, info: stack.meta),
        "links": GraphQLField(ExtraValuesType, resolve=lambda stack, info: stack.links)
    }
)