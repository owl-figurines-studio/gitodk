def check_form_key(form, keys):
    if not isinstance(form, dict):
        form = form.to_dict()
    form_keys = form.keys()
    no_exist_keys = [key for key in keys if key not in form_keys]
    errmsg = ''
    if no_exist_keys:
        errmsg = ",".join(no_exist_keys)
        errmsg = "字段"+errmsg+"不存在"
        print(errmsg)
    return errmsg

