# This class manages the installation and initialisation of a GitLab CI runner.
#
# @param ensure If to install or remove the GitLab CI runner
# @param auto_prerequisites If to automatically install all the prerequisites
#                           resources needed to install the runner
# @param template The path to the erb template (as used in template()) to use
#                 to populate the Runner configuration file. Note that if you
#                 use the runners parameter this file is automatically generated
#                 during runners registration
# @param options An open hash of options you may use in your template
# @param runners An hash which is used to create one or more runners instances.
#                It should be an array of hashes which is passed to the define
#                tools::gitlab::runner
#
class profile::gitlab::runner (
  String                $ensure      = 'present',
  Boolean               $auto_prerequisites = false,
  Boolean               $auto_repo   = false,
  Optional[String]      $template    = undef, # 'profile/ci/gitlab/runner/config.toml.erb',
  Hash                  $options     = { },
  Hash                  $runners     = { },
) {

  $options_default = {
  }
  $gitlab_runner_options = $options_default + $options
  ::tp::install { 'gitlab-runner' :
    ensure             => $ensure,
    auto_prerequisites => $auto_prerequisites,
    auto_repo          => $auto_repo,
  }

  if $template {
    ::tp::conf { 'gitlab-runner':
      ensure       => $ensure,
      template     => $template,
      options_hash => $gitlab_runner_options,
    }
  }

  if $runners != {} {
    $runners.each | $k , $v | {
      tools::gitlab::runner { $k:
        * => $v,
      }
    }
  }
}
