class ReadOnlyFieldsFormMixin:
    readonly_fields = ()

    def apply_readonly_fields(self):
        for field_name in self.readonly_fields:
            self.fields[field_name].widget.attrs["readonly"] = True
