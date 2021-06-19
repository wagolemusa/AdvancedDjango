from django import forms

class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	# perent_id = forms.IngeterField(widget=froms.HiddenInput, required=False)
	content = forms.CharField(widget=forms.Textarea)