from graphql import GraphQLObjectType, GraphQLField, GraphQLString, GraphQLInt, GraphQLList, GraphQLScalarType, \
    GraphQLNonNull, GraphQLInputObjectType, GraphQLInputField


from .query.service import ServiceType, resolve_services

PortsType = GraphQLObjectType(
    name="Ports",
    fields={
        "internal": GraphQLField(GraphQLString, resolve=lambda x, i: x[1]),
        "external": GraphQLField(GraphQLString, resolve=lambda x, i: x[0])
    }
)



VarsType = GraphQLScalarType(
    name="Vars",
    serialize=lambda x: x
)



VarInputType = GraphQLInputObjectType(
    name="StackVar",
    fields={
        "name": GraphQLInputField(GraphQLNonNull(GraphQLString)),
        "value": GraphQLInputField(GraphQLString),
    }
)