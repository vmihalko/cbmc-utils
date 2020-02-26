int main( void ) {
	int a = 4;
	int array[5];
	int i = 0;
	while( a ) {
		i += array[a];
		a--;
	}
	return a;
}
