
def error_checker(request,form,fr):
    allcsv = request.user.csvtoxml.all()
    if request.FILES['file_from'].name.split(".")[1] != fr:
        form.add_error("file_from","This is not a " +fr+" file! Please check the file what you send!")
    for item in allcsv:
        if item.file_from.name.split("/")[1] == request.FILES['file_from'].name:
            form.add_error("file_from","You already converted this file! Check your history of convertion!")