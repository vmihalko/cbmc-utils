int foo() {
	int a[2];
	int c[3];
	int i=5;
	int b;
	while(i > 0) {
		i -= 1;
		b = c[i];
	}
	/*while(i < 5) {
		i += 1;
		b = a[i];
	}*/
	return b;
}
