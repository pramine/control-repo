from fabric.api import *

@task
def setup():
  """Setup the contro-repo, installs r10k, external modules and optional tools"""
  local( "bin/puppet_setup.sh" )

@task
def apply():
  """Run puppet apply (needs to have this control-repo deployed)"""
  sudo( '$(puppet config print codedir)/environments/production/bin/papply.sh ; echo $?' )


@task
def apply_local(role):
  """Run puppet apply locally from the repo directory using the specified role"""
  local( "export FACTER_role=" + str(role) + " && bin/papply_local.sh" )

@task
def apply_noop():
  """Run puppet apply in noop mode (needs to have this control-repo deployed)"""
  sudo( '$(puppet config print codedir)/environments/production/bin/papply.sh --noop ; echo $?' )

@task
@parallel(pool_size=4)
def agent():
  """Run puppet agent"""
  sudo( 'puppet agent -t ; echo $?' )

@task
@parallel(pool_size=4)
def agent_noop():
  """Run puppet agent in noop mode"""
  sudo( 'puppet agent -t --noop ; echo $?' )

@task
@parallel(pool_size=4)
def current_config():
  """Show currenly applied version of our Puppet code"""
  sudo( 'cat $(puppet config print lastrunfile) | grep "config: " | cut -d ":" -f 2- ' )

@task
def deploy_controlrepo():
  """Deploy this control repo on a node (Puppet has to be already installed)"""
  put( "bin/puppet_deploy_controlrepo.sh","/usr/local/bin/puppet_deploy_controlrepo.sh",mode=755 )
  sudo ( "/usr/local/bin/puppet_deploy_controlrepo.sh" )

@task
def install():
  """Install Puppet 4 on a node (for Puppet official repos)"""
  put( "bin/puppet_install.sh","/usr/local/bin/puppet_install.sh",mode=755 )
  sudo ( "/usr/local/bin/puppet_install.sh" )

@task
def module_generate(module=''):
  """Generate a Puppet module based on skeleton"""
  local( "bin/puppet_module_generate.sh " + str(module) )
