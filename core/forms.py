from django import forms


class StyledFormMixin:
    input_class = "form-control"
    select_class = "form-select"
    textarea_class = "form-control form-textarea"
    checkbox_class = "form-check-input"

    def apply_bootstrap_classes(self):
        for field in self.fields.values():
            widget = field.widget
            current_class = widget.attrs.get("class", "")

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = f"{current_class} {self.checkbox_class}".strip()
                continue

            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = f"{current_class} {self.select_class}".strip()
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = f"{current_class} {self.textarea_class}".strip()
                widget.attrs.setdefault("rows", 5)
            else:
                widget.attrs["class"] = f"{current_class} {self.input_class}".strip()

            widget.attrs.setdefault("placeholder", field.label)
