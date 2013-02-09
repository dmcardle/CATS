import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/** 
 * use this class to translate array data into a lilypond file
 * 
 * @author russel
 *
 */
public class dataToLy {
  // array [beats] [notes 
	private char[][] notes;
	private char[][] rhythms;
	private int primaryBeat;
	
	public static void main(String[] args) {
		dataToLy a = new dataToLy();
		a.defineMusic();
		a.write();
	}
	
	// in constructor, define number of measures and time signature
	/*public dataToLy(int m, int t1, int t2){
		primaryBeat = t2;
		notes = new char[m][t1];
		rhythms = new int[m][t1];
	}*/
	
	public void defineMusic(){
		// this method defines a C Major scale in the usable arrays
		primaryBeat = 4;
		notes = new char[5][4];
		rhythms = new char[5][4];
		// initialize 
		for (int i=0; i<5; i++){
			for (int j=0; j<4; j++){
				notes[i][j] = 'Z'; //use Z as flag value 
				rhythms[i][j] = 'Z';
			}
		}
		// write c major scale 
		notes[0][0] = 'c';
		notes[0][1] = 'd';
		notes[0][2] = 'e';
		notes[0][3] = 'f';
		notes[1][0] = 'g';
		notes[1][1] = 'a';
		notes[1][2] = 'b';
		notes[1][3] = 'c';
		notes[2][0] = 'd';
		notes[2][1] = 'c';
		notes[2][2] = 'b';
		notes[2][3] = 'a';
		notes[3][0] = 'g';
		notes[3][1] = 'f';
		notes[3][2] = 'e';
		notes[3][3] = 'd';
		notes[4][0] = 'c';
		rhythms[0][0] = '4';
		rhythms[0][1] = '4';
		rhythms[0][2] = '4';
		rhythms[0][3] = '4';
		rhythms[1][0] = '4';
		rhythms[1][1] = '4';
		rhythms[1][2] = '4';
		rhythms[1][3] = '4';
		rhythms[2][0] = '4';
		rhythms[2][1] = '4';
		rhythms[2][2] = '4';
		rhythms[2][3] = '4';
		rhythms[3][0] = '4';
		rhythms[3][1] = '4';
		rhythms[3][2] = '4';
		rhythms[3][3] = '4';
		rhythms[4][0] = '1';

	}
	
	//write to file 
	public void write() {
		try {
			String beginning = ((char)92)+"version "+((char)34)+"2.14.0"+((char)34)+
					'\n'+((char)92)+"relative c' {\n";
			File file = new File("/home/russel/Documents/workspace/AItests/testing.ly");
 
			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}
 
			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write(beginning);
			for (int i=0; i<5; i++){
				for (int j=0; j<4; j++){
					if (notes[i][j]!='Z' && rhythms[i][j]!='Z'){
						bw.write((char)notes[i][j]+""+(char)rhythms[i][j]+" ");
					}
				}
			}
			bw.write("\n}");
			bw.close();
 
			System.out.println("Done");
 
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
