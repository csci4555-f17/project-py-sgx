from sys import platform as running_platform


class ABI:
    def __init__(self, platform=running_platform):

        if platform == "linux" or platform == "linux2":
            self.platform = "linux"
            self.required_offset = 0
            self.symbol_prefix = ""

        elif platform == "darwin" or platform == "mac" or platform == "macos":
            self.platform = "macos"
            # MacOS requires a 16 byte alignment for function calls.
            # See: https://developer.apple.com/library/content/documentation/DeveloperTools/Conceptual/LowLevelABI/130-IA-32_Function_Calling_Conventions/IA32.html#//apple_ref/doc/uid/TP40002492-SW4
            self.required_offset = 16
            # MacOS adds one underscore before the C name to create an asm label
            self.symbol_prefix = "_"

        else:
            raise RuntimeError("Platform abi not implemented.", platform)

    def label(self, label):
        # type: (str) -> str
        """
        Changes a label to conform to the Application Binary Interface of the
        current OS.
        """
        return self.symbol_prefix + label

    def padding_before_call(self, curr_offset, params_bytes):
        # type: (int, int) -> int
        # python throws exception on `x % 0`
        if self.required_offset == 0:
            padding = 0
        else:
            padding = (self.required_offset - (curr_offset + params_bytes) % self.required_offset) % self.required_offset
        return padding


abi = ABI()


def set_abi(platform):
    abi.__init__(platform)
