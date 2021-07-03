from ast import literal_eval
from configparser import ConfigParser, NoSectionError, NoOptionError, DuplicateSectionError
from os import path

class LoadSettings:
    """
    Usage:
    - Loading:
        loading = LoadSettings()
        loading.open_settings(x,y,z)
        variable = loading.load_settings()
    - Saving:
        loading = LoadSettings()
        loading.save_settings(x,y,z)
    - Deleting:
        loading = LoadSettings()
        loading.delete_settings(x, y)
    """

    def __init__(self):
        self.config = ConfigParser()
        self.filename = f"{path.dirname(__file__)}\\settings.dat"
        self.output = None

    def load_settings(self):
        """
        This function checks if the variable is a literal. If it is, it will be converted to a variable.
        :return: Variable. If not a literal, it won't be converted and returned without changes.
        """
        try:
            self.output = literal_eval(self.output)
        except (ValueError, SyntaxError):
            # If we get an error, the variable does not need to be converted, so we pass.
            pass
        return self.output

    def open_settings(self, section, name, fallback="None"):
        """
        Try to access variable from the config file. If it does not exist or is not readable,
        take the default value

        :param section: The section the value is stored in
        :param name: The name of the variable
        :param fallback: The value that should be used, if there is no variable stored with that name
        :return: -
        """

        try:
            print()
            self.config.read(self.filename)
            self.output = self.config.get(section, name, fallback=fallback)
        except OSError as Error:  # If there is an OSError, try to create the file.
            print(Error)
            try:
                file = open(self.filename, "w")
                file.close()
                self.config.read(self.filename)
                self.output = self.config.get(section, name, fallback=fallback)
            except Exception as Error:
                print(Error, "Could not create settings file")

    def save_settings(self, section, name, variable):
        """
        Store a new variable to the settings file or overwrite an existing one.

        :param section: The section the value is stored in
        :param name: The name of the variable
        :param variable: The value of the variable
        :return: -
        """
        self.config.read(self.filename)
        try:  # If section already exists, pass
            self.config.add_section(section)
        except DuplicateSectionError:
            pass

        self.config.set(section, name, f"{variable}")  # Set up configparser for saving.
        try:  # Show an error if it is not possible to save.
            file = open(self.filename, "w")
            self.config.write(file)
            file.close()
        except(FileNotFoundError, OSError) as Error:
            print(Error, "Could not open file")

    def delete_section(self, section):
        """
        Remove a section.

        :param section: The section that should be removed.
        :return: -
        """
        try:
            file = open(self.filename, "w")
            self.config.remove_section(section)
            file.close()
        except (NoOptionError, NoSectionError, OSError):
            pass

    def delete_settings(self, section, name):
        """
        Remove a variable.

        :param section: The section in which the setting should be removed.
        :param name: The setting that should be removed.
        :return: -
        """
        try:
            file = open(self.filename, "w")
            self.config.remove_option(section, name)
            file.close()
        except (NoOptionError, NoSectionError, OSError) as error:
            print(error)


if __name__ == "__main__":
    loading = LoadSettings()
    print("Please import 'LoadSettings' into your project to use it. See the readme.md for an example.")
