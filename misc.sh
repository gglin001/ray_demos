###############################################################################

# need `[default]` for `ray list nodes` on local machine
pip install ray[default]

###############################################################################

mkdir -p _demos

args=(
  --help
)
ray "${args[@]}" >_demos/ray.help.log
ray start "${args[@]}" >_demos/ray.start.help.log
ray list "${args[@]}" >_demos/ray.list.help.log

###############################################################################

ray status

ray list
ray list actors
ray list actors --detail
ray list jobs --detail
ray list placement-groups --detail
ray list nodes
ray list nodes --detail
ray list workers
ray list tasks
ray list tasks --detail --filter TASK_ID=011ae9488efe4e253ddd4b4e2583d3c2742f223804000000
ray list objects
ray list runtime-envs

ray stop

###############################################################################
