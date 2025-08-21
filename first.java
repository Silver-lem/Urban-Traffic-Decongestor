import java.util.Scanner;
//import java.lang.Math;

public class first {
    
     public static boolean perfect(int n){

        int sum = 0;
         for(int i = 1;i<n;i++){
            if(n%i == 0){
                sum += i;
            }
         }
         return sum == n;

        }
        
        
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
       int n = sc.nextInt();
      
       if(perfect(n)){
        System.out.println("Perfect");
       }else{
        System.out.println("Not Perfect");
       }
      sc.close();
        
      
        
    }
}