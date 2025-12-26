You are extracting data from a Maharashtra Index-II property registration document.

CRITICAL INSTRUCTIONS:

Step 1: Identify the two name fields in the document

* Field (7) is labeled with number "(7)" on the left side
* Field (8) is labeled with number "(8)" on the left side
* These are two SEPARATE fields
* Do NOT mix content from field (7) and field (8)

Step 2: Understand which field is which

* Field (7) = विक्रेता (Seller)
* Field (8) = खरेदीदार (Buyer)

Step 3: Extract separately

* Extract names ONLY from field (7) and put in विक्रेता_नाव
* Extract names ONLY from field (8) and put in खरेदीदार_नाव
* Do NOT combine or mix fields

EXTRACTION PROCESS:

Task 1 - Document Number:
Location: Top right corner after "दस्त क्रमांक :"
Action: Copy the number exactly

Task 2 - Seller Names (विक्रेता_नाव):
Step A: Find the section marked "(7)" on the left margin
Step B: Read ONLY the content within field (7)
Step ![😄]() Find "नाव:-" or "नाव:" in field (7)
Step ![😧]() Extract name(s) after "नाव:-"
Step E: Stop at comma or "पत्ता"
Step F: If multiple names numbered "1):" "2):", extract all from field (7) only
Step G: Do NOT include any names from field (8)

Task 3 - Buyer Names (खरेदीदार_नाव):
Step A: Find the section marked "(8)" on the left margin (below field 7)
Step B: Read ONLY the content within field (8)
Step ![😄]() Find "नाव:-" or "नाव:" in field (8)
Step ![😧]() Extract name(s) after "नाव:-"
Step E: Stop at comma or "पत्ता"
Step F: If multiple names numbered "1):" "2):", extract all from field (8) only
Step G: Do NOT include any names from field (7)

Task 4 - Survey Details:
Find field "(4)" and extract complete text

SPELLING RULES:

Rule 1: Copy each Devanagari character exactly as shown
Rule 2: Preserve all matras precisely:

* ि (short i - before consonant)
* ी (long i - after consonant)
* े (e - one line above)
* ै (ai - two lines above)
* ु (short u - below)
* ू (long u - below)
* ो (o - right side)
* ौ (au - right side with tail)

Rule 3: Preserve special marks: ं (anusvara), ः (visarga), ् (halant)

Rule 4: Do not correct, interpret, or modify spelling

Rule 5: Common errors to avoid:

* Do NOT change े to ी or vice versa
* Do NOT change ि to ी or vice versa
* Do NOT change व to ब or vice versa
* Do NOT change र to ल or vice versa

OUTPUT FORMAT:

{
"document_number": "exact number",
"seller": ["names ONLY from field 7"],
"buyer": ["names ONLY from field 8"],
"property_address_with_gat_numbers": "text from field 4"
}

Where:
( document_number ==दस्त_क्रमांक, seller==विक्रेता_नाव, buyer==खरेदीदार_नाव, property_address_with_gat_numbers == भू_मापन_विवरण)

VERIFICATION CHECKLIST:

Before submitting your answer:
□ Did I extract field (7) content into विक्रेता_नाव?
□ Did I extract field (8) content into खरेदीदार_नाव?
□ Did I keep fields (7) and (8) completely separate?
□ Did I extract only names, not addresses?
□ Did I copy spelling exactly without changes?
□ Is each matra correct?
□ Did I preserve all ं ः ् marks?

IMPORTANT: If field (7) has name "X" and field (8) has name "Y", then विक्रेता_नाव should contain ONLY "X" and खरेदीदार_नाव should contain ONLY "Y". Do not put both X and Y in the same field.

Extract names with exact spelling from the document.
