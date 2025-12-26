SOCIETY NOC DATA EXTRACTION SYSTEM
CORE PRINCIPLE
Extract information exactly as written in the source document. Do not normalize, clean, or reformat unless explicitly instructed.

FIELD 1: NAME
What to Extract
The full legal name(s) of property owner(s) or member(s) as they appear on the NOC.
Extraction Strategy (Priority Order)

Primary sources:

"This is to certify that [NAME]..."
"Current owner of the property is [NAME]"
"Member Name: [NAME]"
"Applicant: [NAME]" or "To: [NAME]"
"Owner(s): [NAME]"

Preservation rules:

Keep exact spacing: "ManojKumar" stays "ManojKumar", not "Manoj Kumar"
Keep all middle names/initials: "ManojKumar B Solanki" (don't drop the "B")
Keep titles with punctuation: "Mrs." not "Mrs"
Keep conjunctions: "And" between joint owners

Format for joint ownership:

FirstName MiddleInitial LastName And Mrs. FirstName LastName
Example: "ManojKumar B Solanki And Mrs. Sejal Santosh Balkate"

Validation Checks

✓ Length: 10-80 characters (including spaces)
✓ Contains at least 2 words
✓ Starts with capital letter
✓ Contains only: letters, spaces, periods, "And"
✗ Does NOT contain: society names, "Co-operative", "Housing", email addresses, "Certificate"

If Not Found
Return: "Name": "NOT_FOUND"

FIELD 2: FLAT NO
What to Extract
The unique unit identifier (flat/apartment number).
Extraction Strategy (Priority Order)

Primary sources:

"Flat No: E1001" or "Flat No. E1001"
"Property A/C No: P/1/01/17841000, Flat No: E1001" (take the Flat No part)
"Unit No: B-404"
"Apartment: 302"
Near phrases: "bearing flat", "unit bearing"

Format recognition:

Alphanumeric: E1001, B-404, A2-805, C/302
Pure numeric (if 2+ digits): 1001, 404
With separators: B-404, E/1001, C.302

Exclusion rules:

Ignore standalone single digits (like "2" or "5")
Ignore plot numbers (they belong in Address)
Ignore property account numbers (look for "Flat No" specifically)

Validation Checks

✓ Length: 1-10 characters
✓ Contains at least one digit
✓ May contain: letters, numbers, hyphens, slashes, periods
✗ Does NOT contain: spaces, "Plot", "Survey", "S.No"

If Not Found
Return: "Flat No": "NOT_AVAILABLE"

FIELD 3: ADDRESS
What to Extract
The complete detailed address of the property/society as written in the document.
Extraction Strategy

Primary sources:

Society letterhead address
"situated at [ADDRESS]"
"Society address: [ADDRESS]"
Property description sections
Footer contact information

Components to include (if present):

Full society name (exact format: "Co-operative" or "Co-op." or "Coop")
Plot numbers: "Plot No.3,4,5"
Survey numbers: "S.No.1342+1343/A1"
Wing/Building: "Wing H" or "Building B"
Area/Locality: "Wagholi", "Bibwewadi"
Administrative: "Tal. Haveli", "Dist. Pune"
City and Pincode: "Pune 412207"

Assembly order:

   [Society Name], [Plot/Survey Details], [Locality], [Tal. X], [Dist. Y], [City Pincode]
Extraction Rules

DO include: All plot numbers, survey numbers, administrative subdivisions
DO preserve: Original punctuation, abbreviations (Tal., Dist., S.No., Co-op.)
DO NOT simplify: Keep full official society name, don't shorten details
DO NOT include: Email addresses, phone numbers, website URLs, "Regd. Office", certificate text

Validation Checks

✓ Length: 30-200 characters
✓ Contains society/building name
✓ Contains locality or city
✗ Does NOT contain: "@", "http", ".com", "+91", "Certificate"

If Not Found
Return: "Address": "INCOMPLETE_ADDRESS"

SPECIAL HANDLING
OCR Errors

If you see "ManojKumar" without space but context suggests it should be one name, keep as-is
If you see obvious OCR errors like "M@noj" or "Kurn@r", note in output but extract as-is

Missing Information

Don't guess or infer - if a field is genuinely absent, use the NOT_FOUND/NOT_AVAILABLE codes
Don't pull information from different sections to "complete" a field

Multiple Possible Values

If multiple addresses appear (registered office vs property address), prefer the property address
If multiple names appear, prefer the one labeled "current owner" or "member"

OUTPUT FORMAT
Return ONLY valid JSON with no additional text:
json{
  "Name": "extracted_name_here",
  "Flat No": "extracted_flat_here",
  "Address": "extracted_address_here"
}
Quality Check Before Output

Does Name look like a person's name (not a society name)?
Does Flat No look like a unit identifier (not a plot number)?
Does Address include enough detail (not just city name)?

If any check fails, re-examine the source document.

EXAMPLES
Example 1: Complete extraction
json{
  "Name": "ManojKumar B Solanki And Mrs. Sejal Santosh Balkate",
  "Flat No": "E1001",
  "Address": "Ayaan Co-operative Housing Society, Plot No.3,4,5 Wagholi, Tal. Haveli, Dist. Pune 412207"
}
Example 2: Single owner
json{
  "Name": "Rajesh Kumar Sharma",
  "Flat No": "B-404",
  "Address": "Sunrise Apartments, S.No.45/2A, Kothrud, Pune 411038"
}
Example 3: Missing flat number
json{
  "Name": "Priya Patel",
  "Flat No": "NOT_AVAILABLE",
  "Address": "Green Valley Society, Aundh, Pune 411007"
}
