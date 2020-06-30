import argparse
import sys

from . import __version__

from .main import AnsibleBuilder
from . import constants


def prepare(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='ansible-builder')
    parser.add_argument(
        '--version', action='version', version=__version__,
        help='Print ansible-builder version and exit.'
    )
    # TODO: Need to have a paragraph come up when running `ansible-builder -h` that explains what Builder is/does
    subparsers = parser.add_subparsers(help='The command to invoke.', dest='action')

    create_command_parser = subparsers.add_parser('create',
                                                  help='Outputs a build context, including a Containerfile, populated with dependencies.')

    build_command_parser = subparsers.add_parser('build',
                                                 help='Builds the container with the Containerfile that got created via "create" command.')
    # TODO: Need to update the docstrings for the create and build commands to be more specific/helpful

    build_command_parser.add_argument('-t', '--tag',
                                      default=constants.default_tag,
                                      help='The name for the container being built.')

    for p in [create_command_parser, build_command_parser]:

        p.add_argument('-f', '--file',
                       default=constants.default_file,
                       dest='filename',
                       help='The definiton of the execution environment.')

        p.add_argument('-b', '--base-image',
                       default=constants.default_base_image,
                       help='The parent image for the execution environment.')

        p.add_argument('-c', '--context',
                       default=constants.default_build_context,
                       dest='build_context',
                       help='The directory to use for the build context. Defaults to $PWD/context.')

        p.add_argument('--container-runtime',
                       default=constants.default_container_runtime,
                       help='Specifies which container runtime to use.')

    args = parser.parse_args(args)

    return AnsibleBuilder(**vars(args))


def run():
    ab = prepare()

    print('Processing...', end='\r')
    # TODO: stdout that prints in real-time and/or a "spinner"

    build_or_create = getattr(ab, ab.action)
    if build_or_create():
        print("Complete! Build context is at: {}".format(ab.build_context))
        sys.exit(0)

    print("An error has occured.")
    sys.exit(1)