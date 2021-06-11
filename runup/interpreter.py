# Built-in
from abc import ABC, abstractmethod
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

# 3rd party
import click

# Own
from runup.runupdb import RunupDB
from runup.utils import vCall, vInfo, vResponse


class Procedure:
    """Describe the properties of the procedures"""

    def __init__(self, name):
        self._name:str = name
        self._cron:str = '0 * * * *'
        self.running:bool = False
        self.source:str = '.'

    @property
    def cron(self):
        return self._cron

    @cron.setter
    def cron(self, schedule:str):
        if re.search():
            self._cron=schedule
        else:
            click.echo('Invalid cron')

    @property
    def name(self):
        return self._name



class Interpreter(ABC):
    """Interpreters' abstract class."""

    @abstractmethod
    def __init__(self, context:Path, verbose:bool, version:str, required_parameters:List[str], 
                valid_parameters:List[str]) -> None:
        """Set interpreter variables."""
        self._context:Path = context
        self._required_parameters:List[str] = required_parameters
        self._valid_parameters:Dict[str, Any] = valid_parameters
        self._verbose:bool = verbose
        self._version:str = version
        
    @abstractmethod
    def create_backup(self) -> bool:
        """Create a new backup."""
        raise NotImplementedError()
        
    @abstractmethod
    def restore_backup(self, backup_id:str) -> bool:
        """Restore the specified backup."""
        raise NotImplementedError()

    @abstractmethod
    def set_environment(self) -> bool:
        """Create the backup enviroment."""
        raise NotImplementedError()

    @abstractmethod
    def missing_parameter(self, yaml_config:Dict[str, Any]) -> Optional[str]:
        """Find the required parameters missing on YAML file"""
        raise NotImplementedError()

    @abstractmethod
    def validate_parameters(self, yaml_config:Dict[str, Any], prefix:str='') -> Optional[str]:
        """Finds the parameters in YAML file not accepted by the interpreter"""
        result:Optional[str] = None
        valid_parameters:Dict[str] = self._valid_parameters.keys()

        if prefix != '':
            prefix = f'{prefix}.'
            vInfo(self._verbose, f'New prefix `{prefix}`')

        if type(yaml_config) == list:
            for value in yaml_config:
                vInfo(self._verbose, f'Testing parameter `{value}`')
                full_key:str = ''
                if f'{prefix}*' in valid_parameters:
                    vInfo(self._verbose, f'`{value}` has been found as `{prefix}*`')
                    full_key = f'{prefix}*'
                elif f'{prefix}{value}' in valid_parameters:
                    full_key = f'{prefix}{value}'
                    vInfo(self._verbose, f'`{value}` has been found as `{prefix}{value}`')

                if len(full_key) > 0:
                    vInfo(self._verbose, f'The value of parameter `{full_key}` is type {type(value)}')
                    if type(value) == self._valid_parameters[full_key]:
                        vInfo(self._verbose, f'`{type(value)}` is a valid type for parameter `{full_key}`')
                    else:
                        click.echo(f'`{value}` expected to be type `{self._valid_parameters[full_key]}` but received `{type(value)}`')
                        return full_key
                else:
                    vInfo(self._verbose, f'`{value}` is not a valid parameter')
                    return full_key

        elif type(yaml_config) == dict:
            for key, values in yaml_config.items():

                vInfo(self._verbose, f'Testing parameter `{key}`')
                full_key:str = ''
                if f'{prefix}*' in valid_parameters:
                    vInfo(self._verbose, f'`{key}` has been found as `{prefix}*`')
                    full_key = f'{prefix}*'
                elif f'{prefix}{key}' in valid_parameters:
                    full_key = f'{prefix}{key}'
                    vInfo(self._verbose, f'`{key}` has been found as `{prefix}{key}`')

                if len(full_key) > 0:
                    vInfo(self._verbose, f'The value of parameter `{prefix}{key}` is type {type(values)}')
                    if type(values) == self._valid_parameters[full_key]:
                        vInfo(self._verbose, f'`{type(values)}` is a valid type for parameter `{prefix}{key}`')
                    else:
                        click.echo(f'`{key}` expected to be type `{self._valid_parameters[full_key]}` but received `{type(values)}`')
                        return full_key

                    if type(values) == dict or type(values) == list:
                        vInfo(self._verbose, f'Analysing subparameters of `{key}`')
                        vCall(self._verbose, 'Interpreter:validate_parameters')
                        next_prefix:str = f'{prefix}*' if f'{prefix}*' in valid_parameters else f'{prefix}{key}'
                        result = self.validate_parameters(values, next_prefix)
                        vResponse(self._verbose, 'Interpreter:validate_parameters', result)
                        if result is not None:
                            vInfo(self._verbose, f'`{key}` has an invalid subparameter')
                            return result
                else:
                    vInfo(self._verbose, f'`{key}` is not a valid parameter')
                    return full_key

        else:
            raise TypeError(f'`yaml_config` expected to be dict or list, `{type(yaml_config)}` received.')

        return None




class Interpreter_1(Interpreter):
    """Interpreter that implements the rules for YAML version 1.0"""
    
    def __init__(self, context:Path, verbose:bool):
        super(Interpreter_1, self).__init__(
            context=context,
            required_parameters = [
                # 'version', # Already validated to get the right interpreter
                'procedure',
                'procedure.*', # `procedure` needs to have ANY value - not empty
            ],
            valid_parameters = {
                # 'fieldname': type,
                'version': str,
                'procedure': dict,
                'procedure.*': dict,
                'procedure.*.cron': str,
                'procedure.*.encrypt': list,
                'procedure.*.encrypt.*': str,
                'procedure.*.exclude': list,
                'procedure.*.exclude.*': str,
                'procedure.*.include': list,
                'procedure.*.include.*': str,
                'procedure.*.password': str,
            },
            verbose=verbose,
            version='1',
        )

    def create_backup(self) -> bool:
        pass

    def restore_backup(self, backup_id:str) -> bool:
        pass

    def missing_parameter(self, yaml_config:Dict[str, Any], search_area:Optional[List[str]]=None) -> Optional[str]:
        
        if search_area is None:
            search_area = self._required_parameters

        for parameter in search_area:
            vInfo(self._verbose, f'Analysing parameter `{parameter}`')
            vCall(self._verbose, f'Interpreter_1:missing_parameter_part')
            missing_part:str = self.missing_parameter_part(yaml_config, parameter)
            vResponse(self._verbose, f'Interpreter_1:missing_parameter_part', missing_part)
            if missing_part:
                vInfo(self._verbose, f'missing parameter part `{missing_part}`')
                return missing_part

        return None

    def missing_parameter_part(self, yaml_config:Dict, parameter:str) -> Optional[str]:
        """Analyse each part of a parameter looking for missing parts."""

        if '.' not in parameter:
            vInfo(self._verbose, f"Parameter `{parameter}` doesn't have sub-paramenters")
            if parameter == '*':
                if yaml_config is not None and len(yaml_config) > 0:
                    vInfo(self._verbose, f"YAML file cointains {len(yaml_config)} parameters.")
                    return None
                elif yaml_config is not None:
                    vInfo(self._verbose, f"YAML file cointains no parameters.")
                    return '*'
                else:
                    vInfo(self._verbose, f"YAML file cointains no parameters.")
                    return None
            elif parameter not in yaml_config.keys():
                vInfo(self._verbose, f"Single parameter `{parameter}` not found in YAML file")
                return parameter
        else:
            vInfo(self._verbose, f"Parameter `{parameter}` have sub-paramenters")

            parts = parameter.split('.', 1)
            if parts[0] not in yaml_config.keys():
                vInfo(self._verbose, f"Parameter part `{parts[0]}` not found in YAML file")
                return parts[0]
            else:
                vInfo(self._verbose, f"Parameter part `{parts[0]}` found in YAML file")
                vCall(self._verbose, f"Interpreter_1:missing_parameter_part")
                missing:str = self.missing_parameter_part(yaml_config[parts[0]], parts[1])
                vResponse(self._verbose, f'Interpreter_1:missing_parameter_part', missing)
                if missing == '*':
                    return f'*{parameter[0:-2]}'
                elif missing is None:
                    return None
                else:
                    return f'{parameter}'

    def set_environment(self) -> bool:
        """
        Create the backup enviroment.

        Creates a directory `.runup` at context level. In it
        creates a `.version` that only contains a number `1`
        and creates a SQLite database named `runup.db`.
        """

        vInfo(self._verbose, 'Setting environment.')

        # Create the directory `.runup`
        if not os.path.exists(f'{self._context}/.runup'):
            os.mkdir(f'{self._context}/.runup')
            vInfo(self._verbose, f'Created directory {self._context}/.runup')
        else:
            vInfo(self._verbose, f'The directory `{self._context}/.runup` already exists.')
            click.echo('RunUp is already initiated.')
            return False
        
        # Create file `.version`
        with open(f'{self._context}/.runup/.version', "w") as file:
            file.write(self._version)
        vInfo(self._verbose, f'Created file {self._context}/.runup/.version')

        # Create database
        RunupDB(self._context, self._verbose).create_database()

        if self._verbose:
            click.echo('-'*10)

        return True

    def validate_parameters(self, yaml_config:Dict[str, Any], prefix:str='') -> bool:
        return super().validate_parameters(yaml_config, prefix)