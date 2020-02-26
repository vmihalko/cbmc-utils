int main( void ) {
	int a = 5;
	int array[5];

	while( a ) {
		a += array[a];
		a--;
	}
	return a;
}
