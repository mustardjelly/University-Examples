
// variables
List<int> primeNumbers = new List<int>();
int amountToFind = 5;
int currentCount = 0;
int[] primeList = new int[amountToFind];

// find primes and add them to primeList (an array)
for (int i = 2; i < Math.Pow(amountToFind, 2); i++) {
	if (currentCount < amountToFind) {
		for (int j = (int)Math.Sqrt(j); j > 0; j--) {
				if (i % j == 0 && j != 1) {
					break;
				}
				if (j == 1) {
					primeList[currentCount] = i;
					currentCount++;
				}

		}
	} else {
		break;
	}
}

// OUTPUT:
Console.WriteLine(primeNumbers.Count);

for (int i = 0; i < primeNumbers.Count; i++){
	Console.WriteLine(primeNumbers[i]);
}
