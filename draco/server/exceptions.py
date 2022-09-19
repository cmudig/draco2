class UnknownDracoPropertyError(AttributeError):
    def __init__(self, property_name):
        self.property_name = property_name
        super().__init__(f"Unknown Draco property: {property_name}")
