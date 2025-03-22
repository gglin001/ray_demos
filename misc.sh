###############################################################################

# need `[default]` for `ray list nodes` on local machine
pip install ray[default]

###############################################################################

mkdir -p _demos

args=(
  start
  --help
)
ray "${args[@]}" >_demos/ray.start.help.log

###############################################################################

ray status
ray list nodes
ray list runtime-envs

ray stop

###############################################################################
