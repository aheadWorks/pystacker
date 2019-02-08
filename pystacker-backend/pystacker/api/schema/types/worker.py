from graphql import GraphQLObjectType, GraphQLField, \
    GraphQLString, GraphQLFloat

WorkerType = GraphQLObjectType(
    name="Worker",
    fields={
        "name": GraphQLField(GraphQLString),
        "interval": GraphQLField(GraphQLFloat)
    }
)


