package jsonmerger;

import java.io.*;
import java.util.*;
import org.json.*;

public class JSONMerge {

	/* -----------------------Helper functions------------------------*/
	
	// Check 2 nodes has same ID
	public static boolean hasSameID(JSONObject left, JSONObject right) {
		if (left.getString("id").equals(right.getString("id"))) {
			return true;
		} else {
			return false;
		}
	}

	// Parse file content to ArrayList of JSON Objects
	// Note JSON objects are stored in JSONArray "response"
	public static void parseJsonArray(ArrayList<JSONObject> jarray, String fileName) {
		try {
			File file = new File(fileName);
			BufferedReader br;
			br = new BufferedReader(new FileReader(file));
			String st;
			while ((st = br.readLine()) != null) {
				JSONObject json = new JSONObject(st);
				JSONArray respond = json.getJSONArray("response"); // grab the "response" Jarray
				for (int i = 0; i < respond.length(); i++) {
					jarray.add(respond.getJSONObject(i));		// "select the JObjects out from the array"
				}
			}
			br.close();
		} catch (FileNotFoundException e) {
			System.out.println("File unreadable!");
		} catch (IOException e) {
			System.out.println("I/O Error!");
		}
	}

	// Update JSONObject "base" with "added"
	public static void updateJsonElement(JSONObject base, JSONObject added) {
		for (String key : base.keySet()) {
			if (added.has(key)) {
				base.put(key, added.get(key));
			}
		}
	}

	// Check if 2 files has same ArticleID
	public static boolean sameArticleID(String file1, String file2) {
		String file1ID = file1.substring(0, file1.indexOf("_"));
		String file2ID = file2.substring(0, file1.indexOf("_"));
		if (file1ID.equals(file2ID)) {
			return true;
		} else {
			return false;
		}
	}

	// compare time stamp of 2 files
	// return 1 if 1 > 2, -1 if 1 < 2, 0 if equals
	public static int compareArticleDate(String file1, String file2) {
		Long date1 = Long.parseLong(file1.substring(file1.indexOf("_") + 1, file1.indexOf(".")));
		Long date2 = Long.parseLong(file2.substring(file2.indexOf("_") + 1, file2.indexOf(".")));
		if (date1 > date2) {
			return 1;
		} else if (date1 < date2) {
			return -1;
		} else {
			return 0;
		}
	}

	// Extract article ID
	public static String getArticleID(String fileName) {
		return fileName.substring(0, fileName.indexOf("_"));
	}
	
	
	/*--------------------main-------------------------*/
	public static void main(String[] args) throws JSONException, IOException {

		File folder = new File("./Disqus file/");
		File[] listOfFiles = folder.listFiles();
		HashMap<String, ArrayList<String>> fileMap = new HashMap<>();

		/*
		 * Add files to map
		 * <ArtilceID> - <ArrayList of filenames> 
		 * */
		for (int i = 0; i < listOfFiles.length; i++) {
			String fileName = listOfFiles[i].getName();
			if (!fileMap.containsKey(getArticleID(fileName))) {
				ArrayList<String> temp = new ArrayList<String>();
				temp.add(fileName);
				fileMap.put(getArticleID(fileName), temp);
			} else if (fileMap.containsKey(getArticleID(fileName))) {
				ArrayList<String> temp = fileMap.get(getArticleID(fileName));
				for (int j = 0; j < temp.size(); j++) {
					if (compareArticleDate(fileName, temp.get(j)) < 0) {  // organize in increasing order
						temp.add(j, fileName);
						break;
					} else if (j == temp.size() - 1) {
						temp.add(temp.size(), fileName);
						break;
					}
				}
				fileMap.put(getArticleID(fileName), temp);
			}
		}
		
		
		/*-------------- Merge files with similar article ID into 1 file --------------*/
		for (String articleID : fileMap.keySet()) {
			ArrayList<String> temp = fileMap.get(articleID);
			ArrayList<JSONObject> jsonArray = new ArrayList<>();
			
			// Loop through array of file names with same articleID
			for (int i = 0; i < temp.size(); i++) {
				String fileName = "./Disqus file/"+ temp.get(i);
				//Put file content to jsonArray if not already did
				if (jsonArray == null) {
					parseJsonArray(jsonArray, fileName);
					// put back into a file
//					
//					String test_File = "./MergedFiles/" + "test.txt";
//					PrintWriter writer = new PrintWriter(test_File, "UTF-8");
//					for(JSONObject element : jsonArray) {
//						writer.println(element.toString());
//					}
//					writer.close();
					
				//Already put, update the jsonArray
				} else {
					ArrayList<JSONObject> jsonUpdate = new ArrayList<>();
					parseJsonArray(jsonUpdate, fileName);
					for (JSONObject updateJsonObject : jsonUpdate) {
						boolean alreadyHad = false;
						for (JSONObject srcJsonObject : jsonArray) {
							if (hasSameID(srcJsonObject, updateJsonObject)) {
								updateJsonElement(srcJsonObject, updateJsonObject);
								alreadyHad = true;
							}
						}
						if(!alreadyHad) {
							jsonArray.add(updateJsonObject);
						}
					}
				}
			}
			
			//Write the final version of jsonArray to file, named with article ID
			String fileNameWithArticleID = "./MergedFiles/" + articleID + ".txt";
			PrintWriter writer = new PrintWriter(fileNameWithArticleID, "UTF-8");
			writer.print("{\"response\":[");
			int count = 0;
			for(JSONObject element : jsonArray) {
				if (count == jsonArray.size() - 1) {
					writer.print(element.toString());
				} else {
					writer.print(element.toString()+",");
				}
				count++;
			}
			writer.print("]}");
			writer.close();
		}

	}
}
