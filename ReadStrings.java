import java.util.Scanner;

public class ReadStrings 
{
	public static void main(String[] args) 
	{
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter three strings(names or words): ");
		String string = scan.next();
		String string1 = scan.next();
		String string2 = scan.next();
		scan.close();
		String nameA = "";
		String nameB = "";
		String nameC = "";
		if (string.compareTo(string1) < 0)
		{
			if(string.compareTo(string2) < 0)
			{
				nameA = string;
				if (string1.compareTo(string2) < 0)
				{
					nameB = string1;
					nameC = string2;
				}
				else
				{
					nameB = string2;
					nameC = string1;
				}
			}
			else
			{
				nameA = string2;
				nameB = string;
				nameC = string1;
			}
		}
		else
		{
			if (string1.compareTo(string2) < 0)
			{
				nameA = string1;
				if (string.compareTo(string2) < 0)
				{
					nameB = string;
					nameC = string2;
				}
				else
				{
					nameB = string2;
					nameC = string;
				}
			}
			else
			{
				nameA = string2;
				nameB = string1;
				nameC = string;
			}
		}
	System.out.printf("%s\n%s\n%s\n",nameA,nameB,nameC);
	}
}
