
/**
 * This class represents a musical note.  Given a frequency in Hertz,
 * it can find the name of the closest musical note and tell you how
 * far away you are from that note.
 * 
 * <h4>Useful links:</h4>
 * <ul>
 *     <li> <a href="http://en.wikipedia.org/wiki/Piano_key_frequencies">Piano Key Frequencies</a></li>
 *     <li> <a href="http://en.wikipedia.org/wiki/Scientific_pitch_notation">Scientific Pitch Notation</a></li>
 * </ul>
 */
public class Note {

    public static final int A1_FREQUENCY = 55;
    private static final double HALF_STEPS_COEFFICIENT = 12 / Math.log(2);
    private double frequency;
    private String closestNote;
    private double distanceFromClosestNote;
    private int halfStepsFromA;

    /**
     * Construct a note with the default frequency of 220 Hz.
     */
    public Note() {
        this(220.0);
    }

    /**
     * Construct a note with specified frequency.
     * @param frequency Frequency of the note in Hertz.
     */
    public Note(double frequency) {
        setFrequency(frequency);
    }

    public Note(Note n) {
        setFrequency(n.frequency);
    }

    /**
     * Set the new frequency of the note.
     * @param newFrequency Frequency in Hertz.
     */
    public void setFrequency(double newFrequency) {
        frequency = newFrequency;
        calcClosestNote();
    }


    public double calcHalfStepsFromA() {
        halfStepsFromA = (int)(Math.log(frequency / A1_FREQUENCY) * HALF_STEPS_COEFFICIENT);
        return halfStepsFromA;
    }
    public double getHalfStepsFromA() {
        return halfStepsFromA;
    }
    public void setHalfStepsFromA(int halfSteps) {
        this.halfStepsFromA = halfSteps;
    }

    /**
     * Find the note name, such as "A" or "A# / Bb".
     * @param halfStepsFromA number of half steps from A
     * @return
     */
    public static String nameOfNote(int halfStepsFromA) {
        String closestNote;
        switch (halfStepsFromA % 12) {
            case 0: closestNote = "A"; break;
            case 1: closestNote = "A# / Bb"; break;
            case 2: closestNote = "B"; break;
            case 3: closestNote = "C"; break;
            case 4: closestNote = "C# / Db"; break;
            case 5: closestNote = "D"; break;
            case 6: closestNote = "D# / Eb"; break;
            case 7: closestNote = "E"; break;
            case 8: closestNote = "F"; break;
            case 9: closestNote = "F# / Gb"; break;
            case 10: closestNote = "G"; break;
            case 11: closestNote = "G# / Ab"; break;
            default: closestNote = "---";
        }
        return closestNote;

    }

    private void calcClosestNote() {

        // Calculate the distance in Hertz
        double distanceFromA = calcHalfStepsFromA();

        // Round to the nearest note
        int halfStepsFromA = (int) (distanceFromA + 0.5);

        closestNote = nameOfNote(halfStepsFromA);

        // Calculate the frequency of the close note
        double frequencyOfClosestNote = calcFrequency(halfStepsFromA);

        // Calculate the distance from the actual note
        distanceFromClosestNote = this.frequency - frequencyOfClosestNote;

    }

    /**
     * Used to calculate the frequency of a specified by its distance from A.
     * @param halfStepsFromA
     * @return frequency in Hertz
     */
    public static double calcFrequency(int halfStepsFromA) {
        return A1_FREQUENCY * Math.pow(2, halfStepsFromA / 12.0);
    }

    /**
     * Get the frequency of this note.
     * @return the stored frequency in Hertz.
     */
    public double getFrequency() {
        return frequency;
    }

    /**
     * Return the name of the note closest to this note.
     * @return the name of the note
     */
    public String getClosestNote() {
        return closestNote;
    }

    /**
     * Get the distance between this note and the note closest to it in Hertz.
     * @return distance in Hertz
     */
    public double getDistanceFromClosestNote() {
        return distanceFromClosestNote;
    }

    /**
     * Give the name of the closest note to this one.
     * @return the name of the closest note
     */
    @Override
    public String toString() {
        return getClosestNote();
    }
}
