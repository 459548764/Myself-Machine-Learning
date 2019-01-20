public class Pv1 
{
    public int sem_produce = 1;
    public int sem_comsume = 0;

    Thread produce = new Thread()
    {
        public void run()
        {
            while(true)
            {
                System.out.println("1-Produce data");
                while(sem_produce <= 0);
                sem_produce--;
                System.out.println("2-Send data to Buffer");
                sem_comsume++;
            }
        }
    };
    
    Thread comsume = new Thread()
    {
        public void run()
        {
            while(true)
            {
                while(sem_comsume <= 0);
                sem_comsume--;
                System.out.println("3-Fetch data from Buffer");
                sem_produce++;
                System.out.println("4-Comsume data");
            }
        }
    };
    
    public static void main(String[] args) 
    {
        Pv1 pv = new Pv1();
        pv.produce.start();
        pv.comsume.start();
    }    
}
