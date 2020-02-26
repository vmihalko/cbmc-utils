int bar() {
	int a[2];
	int i=5;
	int b;
	while(i > 0) { 
		i -= 1;
		b = a[i];
	}
	return b;
}
