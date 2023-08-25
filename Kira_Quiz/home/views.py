from django.shortcuts import render



def welcomepage(request):
	return render(request, 'home/welcomepage.html')

def levels(request):
	return render(request, 'home/levels.html')

def level_0(request):
	return render(request, 'home/level_0.html')

def level_1(request):
	return render(request, 'home/level_1.html')

def level_2(request):
	return render(request, 'home/level_2.html')	
