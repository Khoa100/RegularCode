
    public static double[] roundArray(double array[]){
		double[] rarray = new double[array.length];
		
		for(int i = 0; i< array.length; i++){
			rarray[i] = Math.round(array[i]);
		}
		return rarray;
	}
	
	public static void main(String[] args){
    	//An array of doubles
		double[] myArray={10.1, 10.2, 10.3, 10.4, 10.5}; 
		
		roundArray(myArray);
        
        // user-defined method that uses 
        // enhanced-for loop to print the array
		printArray(myArray); 
        					 

	}
		

