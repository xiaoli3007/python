import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Main {

    public static void main(String[] args) {

        String aa= MD5(MD5("zj123456")+"NetTeaching-zjbar-aclaedu");
        System.out.println(aa);
    }

    private static String  MD5(String plainText ) {
        String s = null;
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(plainText.getBytes());
            byte b[] = md.digest();
            int i;
            StringBuffer buf = new StringBuffer("");
            for (int offset = 0; offset < b.length; offset++) {
                i = b[offset];
                if(i<0) i+= 256;
                if(i<16)
                    buf.append("0");
                buf.append(Integer.toHexString(i));
            }
            //System.out.println("result: " + buf.toString());//32位的加密
           // System.out.println("result: " + buf.toString().substring(8,24));//16位的加密
            s = buf.toString();
        } catch (NoSuchAlgorithmException e) {
// TODO Auto-generated catch block
            e.printStackTrace();
        }
        return s;
    }


}




