from ..query.service import resolve_status

from graphql import GraphQLObjectType, GraphQLField, \
    GraphQLString, GraphQLInt, GraphQLList

PortsType = GraphQLObjectType(
    name="Ports",
    fields={
        "internal": GraphQLField(GraphQLString, resolve=lambda x, i: x[1]),
        "external": GraphQLField(GraphQLString, resolve=lambda x, i: x[0])
    }
)

ServiceType = GraphQLObjectType(
    name="Service",
    fields={
        "name": GraphQLField(GraphQLString),
        "image": GraphQLField(GraphQLString),
        "status": GraphQLField(GraphQLInt, resolve=resolve_status),
        "ports": GraphQLField(GraphQLList(PortsType)),
    }
)
