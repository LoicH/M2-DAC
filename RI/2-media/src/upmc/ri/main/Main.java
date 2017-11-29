package upmc.ri.main;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import upmc.ri.bin.VisualIndexes;
import upmc.ri.index.ImageFeatures;
import upmc.ri.io.ImageNetParser;
import upmc.ri.struct.DataSet;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		System.out.println("Start");
		List<String> files = Arrays.asList("tree-frog.txt", "harp.txt");
		DataSet<double[], String> ds = VisualIndexes.createDatSet(files);
		System.out.println("DataSet created");
		System.out.println("Retrieving n01644373_354");
		List<ImageFeatures> features = null;
		try {
			 features = ImageNetParser.getFeatures("tree-frog.txt");
		} catch (Exception e) {
			System.out.println("Can't read file tree-frog.txt");
			e.printStackTrace();
			System.exit(1);
		}

		ImageFeatures target = null;
		for(ImageFeatures feat : features) {
			if (feat.getiD().equals("n01644373_354")) {
				target = feat;
				System.out.println("Found target");
				break;
			}
		}
		List<Integer> words = target.getwords();
		System.out.println(words);
		Map<String, Integer> wordCount = new HashMap<String, Integer>();

		for(Integer word: words) {
		  Integer count = wordCount.get(word);          
		  wordCount.put(word, (count==null) ? 1 : count+1);
		}
		System.out.println("Over");
	}

}
