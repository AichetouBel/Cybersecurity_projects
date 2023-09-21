while True:
	try:
		list=input('enter a list seperated by espace')
		p=list.split()
		print(p)
		k=n-1
		for i in p:
			j=int(i)
			if j>=2 and j<=n and len(p)==n-1 and k>0:
				print('ok')
				k=k-1
				if k==0:
					break
				else:
					continue
			else:
				print('enter a valid list number')
	except ValueError:
		print('enter a valid list number separated by espace')

print('that very good')
