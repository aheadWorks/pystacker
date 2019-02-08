from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLEnumValue, GraphQLString, \
    GraphQLInt, GraphQLList, GraphQLScalarType,GraphQLNonNull, GraphQLArgument, GraphQLBoolean, GraphQLEnumType


from .schema.types.stack import StackType
from .schema.types.worker import WorkerType

from .schema.subscription.pull_img import subscribe_pull_img, pull_img_type
from .schema.subscription.run_cmd import subscribe_run_cmd, subscribe_run_service_cmd
from .schema.subscription.get_logs import subscribe_get_logs

from .schema.query.worker import resolve_list_workers
from .schema.query.stack import resolve_all_stacks, resolve_one_stack
from .schema.query.template import resolve_get_template, all_templates_resolver

from .schema.mutation.worker import resolve_force_worker
from .schema.mutation.stack import resolve_delete_stack, resolve_create_stack


async def resolve_meta(tpl, info):
    return (await tpl.get_other()).get('meta', {})


TemplateVarsType = GraphQLScalarType(
    name="template_vars",
    serialize=lambda x: x
)


TemplateType = GraphQLObjectType(
    name="template",
    fields={
        "name": GraphQLField(GraphQLString, resolve=lambda x, y: x.path.name),
        "vars": GraphQLField(TemplateVarsType, resolve=lambda x, y: x.get_vars(y.context['app'])),
        "meta": GraphQLField(TemplateVarsType, resolve=resolve_meta),
    }
)

schema = GraphQLSchema(
    query=GraphQLObjectType(
        name='RootQueryType',
        fields={
            'stacks': GraphQLField(
                GraphQLList(StackType),
                resolve=resolve_all_stacks
            ),
            'stack': GraphQLField(
                StackType,
                args={'id': GraphQLArgument(GraphQLNonNull(GraphQLInt))},
                resolve=resolve_one_stack
            ),
            'templates': GraphQLField(
                GraphQLList(TemplateType),
                resolve=all_templates_resolver
            ),
            'template': GraphQLField(
                TemplateType,
                args={'name': GraphQLArgument(GraphQLNonNull(GraphQLString))},
                resolve=resolve_get_template
            ),
            'workers': GraphQLField(
                GraphQLList(WorkerType),
                resolve=resolve_list_workers
            )
        }
    ),
    mutation=GraphQLObjectType(
        name="RootMutationType",
        fields={
            "deleteStack": GraphQLField(
                GraphQLBoolean,
                args={'id': GraphQLArgument(GraphQLNonNull(GraphQLInt))},
                resolve=resolve_delete_stack
            ),
            "createStack": GraphQLField(
                StackType,
                args={
                    'name': GraphQLArgument(GraphQLNonNull(GraphQLString)),
                    'from_template': GraphQLArgument(GraphQLNonNull(GraphQLString)),
                    'vars': GraphQLArgument(GraphQLList(GraphQLList(GraphQLString)))
                },
                resolve=resolve_create_stack
            ),
            "forceWorker": GraphQLField(
                WorkerType,
                args={
                    "name": GraphQLArgument(GraphQLNonNull(GraphQLString))
                },
                resolve=resolve_force_worker
            )
        }
   ),
    subscription=GraphQLObjectType(
        name="RootSubscriptionType",
        fields={
            "runCmd": GraphQLField(
                GraphQLString,
                args={
                    'id': GraphQLArgument(GraphQLNonNull(GraphQLInt)),
                    'cmd': GraphQLArgument(
                        GraphQLEnumType(
                            "Cmd",
                            values={
                                'up': GraphQLEnumValue('up'),
                                'down': GraphQLEnumValue('down'),
                                'pause': GraphQLEnumValue('pause'),
                                'unpause': GraphQLEnumValue('unpause'),
                                'logs': GraphQLEnumValue('logs'),
                                'destroy': GraphQLEnumValue('destroy')
                            }
                        )
                    )
                },
                resolve=lambda x, i, id, cmd: x,
                subscribe=subscribe_run_cmd
            ),
            "execServiceCmd": GraphQLField(
                GraphQLString,
                args={
                    'stack_id': GraphQLArgument(GraphQLNonNull(GraphQLInt)),
                    'service_name': GraphQLArgument(GraphQLNonNull(GraphQLString)),
                    'cmd': GraphQLArgument(GraphQLNonNull(GraphQLString))
                },
                resolve=lambda x, i, stack_id, service_name, cmd: x,
                subscribe=subscribe_run_service_cmd
            ),
            "pullImages": GraphQLField(
                pull_img_type,
                args={
                    'id': GraphQLArgument(GraphQLNonNull(GraphQLInt))
                },
                resolve=lambda x, i, id: x,
                subscribe=subscribe_pull_img
            ),
            "getLogs":  GraphQLField(
                GraphQLString,
                args={
                    'stack_id': GraphQLArgument(GraphQLNonNull(GraphQLInt)),
                    'service_name': GraphQLArgument(GraphQLNonNull(GraphQLString))
                },
                resolve=lambda x, i, stack_id, service_name: x,
                subscribe=subscribe_get_logs
            )
        }
    )
)
