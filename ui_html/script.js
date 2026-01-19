// Document type configurations
const DOCUMENT_TYPES = {
    'Index 2': {
        fields: [
            { name: 'Document_number/ दस्त क्रमांक', type: 'text', isArray: false },
            { name: 'Seller/देनारा', type: 'text', isArray: true },
            { name: 'Buyer/घेणारा', type: 'text', isArray: true },
            { name: 'property_address_with_gat_numbers/ पत्ता', type: 'textarea', isArray: false }
        ]
    },
    'NOC': {
        fields: [
            { name: 'Name', type: 'text', isArray: true },
            { name: 'Flat No', type: 'text', isArray: false },
            { name: 'Address', type: 'textarea', isArray: false }
        ]
    },
    'No Dues': {
        fields: [
            { name: 'Name', type: 'text', isArray: true },
            { name: 'Address', type: 'textarea', isArray: false },
            { name: 'Amount', type: 'text', isArray: false }
        ]
    }
};

// Actual Data - Pre-filled document data for demo (embedded directly)
const ACTUAL_DATA = {
    'Index 2': [
        {
            "Document id": "Document 1",
            "url": "https://drive.google.com/file/d/1o3LcTCCIc1tyBHwWob9y-iAHqGxZ6XK_/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "13862/2021",
            "Seller/देनारा": ["आर्मी वेलफेअर हौसिंग ओर्गनायझेशन तर्फे सूर्यवंशी अमरनाथ विश्वास"],
            "Buyer/घेणारा": ["प्रशांतचंद्र छोटेलाल अग्रवाल", "संतोष अग्रवाल"],
            "property_address_with_gat_numbers/ पत्ता": "न इतर माहिती:, इतर माहिती: मौजे वाघोली तालुका हवेली जिल्हा पुणे येथिल जुना गट नं 1454 / 114547 2 1455 यांसी नवीन गट न 1455/1454/1/1454/2 या मिळकतीवर बांधण्यात आलेल्या ए. डब्लु.एच.ओ. विजय विहार या नावाने असणाऱ्या प्रकल्पातील बी विंग मधील चौथ्या मजल्यावरील सदनिका नं 404 यांसी कार्पेट क्षेत्र 1077 चौ फूट तसेच बाल्कनी क्षेत्र 78 चौ फूट व टेरेस क्षेत्र 37 चौ फूट तसेच कव्हर्ड कार पार्किंग न मी मी पी पी 147 क्षेत्र 134 चौ फूट या मिळकती बाबत (( GAT NUMBER : 1454/1 1454/2 1455 ))"
        },
        {
            "Document id": "Document 2",
            "url": "https://drive.google.com/file/d/1CP05HUszWp70rYKo4I3vIyh9T23ydyRy/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "5655/2025",
            "Seller/देनारा": ["संदीप बालाजी विधाते", "अश्विनी संदीप विधाते (लग्नानंतरचे नाव) अश्विनी दिगंबर टकले (लग्नापूर्वीचे नाव)"],
            "Buyer/घेणारा": ["दीपक सरकार", "संजुक्ता बोस"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे म.न.पा. इतर वर्णन:, इतर माहिती: गाव मौजे वाघोली, ता. हवेली, जि. पुणे येथील मिळकत गट नं. 625 यांची क्षेत्र 00 हे 82 आर यावर बांधण्यात आलेल्या \"स्पंदन स्पर्श को. ऑप. हौसिंग सोसायटी लि.\" या मधील बिल्डिंग/विंग ए मधील चौथ्या मजल्यावरील फ्लॅट नं. 407 यांची क्षेत्र 612 चौ.फुट म्हणजेच 56.88 चौ.मी. तसेच लगतचे टेरेस क्षेत्र 75 चौ.फुट म्हणजेच 6.97 चौ.मी. कारपेट ही फ्लॅट मिळकत (( GAT NUMBER : 625, Flat No. 407 ))"
        },
        {
            "Document id": "Document 3",
            "url": "https://drive.google.com/file/d/13VHasFQZ7b36zXnYAvTq4nna7M0Gl1bo/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "6531/2025",
            "Seller/देनारा": ["किरण बासुदेव नायक"],
            "Buyer/घेणारा": ["योगेश अनिल थोरात", "माधुरी योगेश थोरात"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे म.न.पा. इतर वर्णन, इतर माहिती: मौजे वाघोली येथील गट नं. 564 यांसी ऐकून क्षेत्र 10 हे 23 आर पोट्वरब्यासह यासी आकार 46 रु 69 पैसे पैकी मान्यता देणार न. 1 यांचे हिश्याचे क्षेत्रापैकी 05 हे 60 आर तसेच गट नं. 559/1 यांसी ऐकुण क्षेत्र 13 हे 58 आर पैकी मान्यता देणार न. 2 यांचे हिश्याचे क्षेत्र 0 हे 05 आर असे एकत्रित क्षेत्र 05 हे 65 आर या मिळकतिवरिल नियोजित मॅजेस्टिक सिटी या प्रकल्पामधील विंग बी मधील आठव्या मजल्यावरील फ्लॅट नं. 802 यांसी क्षेत्र 50.88 चौ.मी. (कार्पेट) तसेच लगतचे टेरेस क्षेत्र 11.42 चौ.मी. एकूण 62.30 चौ.मी. (( GAT NUMBER : 564 ))"
        },
        {
            "Document id": "Document 4",
            "url": "https://drive.google.com/file/d/1owni13xOnrkiVJSvTILlDXGNsmZw1DME/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "13553/2019",
            "Seller/देनारा": ["गांधी बाफना कन्स्ट्रक्शन्स प्रा. लि. कंपनी तर्फे अधिकृत स्वाक्षरीकरीता डायरेक्टर श्री. योगेश अजित बाफना यांचे तर्फे कु. मु. म्हणून श्री. अशोक राचलवार", "मान्यता देणार श्री. योगेश आनंदपाल गोयल"],
            "Buyer/घेणारा": ["मनोजकुमार बी. मोलंकी", "सेजल संतोष बळकटे"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे. गाव मौजे वाघोली (आव्हाळवाडी) ता. हवेली जि. पुणे. गट नं. 1342+1343/ए/1 येथील \"अयान\" प्रोजेक्ट मधील बिल्डिंग नं. 2 मधील दहाव्या मजल्यावरील फ्लॅट नं. E-1001 यांसी क्षेत्र 46.5 चौ.मी. म्हणजेच 500.50 चौ.फुट कार्पेट तसेच बाल्कनी व टेरेस (( GAT NUMBER : 1342 ))"
        },
        {
            "Document id": "Document 5",
            "url": "https://drive.google.com/file/d/1OUlu6ES0pqDJFmswwQZ-2nENiKFuYtWQ/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "7180/2011",
            "Seller/देनारा": ["मेसर्स आर्यन डेव्हलपर्स"],
            "Buyer/घेणारा": ["भारत बाळासाहेब जगदाळे", "सौ सिमा भारत जगदाळे"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: हवेली. गाव मौजे वाघोली गट नं. 1173 येथील नियोजित मयुरी गार्डन प्रोजेक्ट मधील बिल्डींग नं. बी मधील चौथ्या मजल्यावरील फ्लॅट नं. 26 यांसी क्षेत्र 560 चौ.फुट किंवा 52.04 चौ.मी. बिल्टअप तसेच लगतचे टेरेस क्षेत्र 60 चौ.फुट किंवा 5.57 चौ.मी."
        },
        {
            "Document id": "Document 6",
            "url": "https://drive.google.com/file/d/1FRrj59OzU73SO9sOrWAG7v3TaPdaHyEu/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "8182/2024",
            "Seller/देनारा": ["अजय कुमार साहू", "महिस्मिता साहू"],
            "Buyer/घेणारा": ["प्रणव नवनाथ दिघे"],
            "property_address_with_gat_numbers/ पत्ता": "गट नं. 910 (जुना गट नं. 911) यासी क्षेत्र 00 हे 25 आर, गट नं. 911 (जुना गट नं. 912) यासी क्षेत्र 00 हे 16 आर, गट नं. 912 (जुना गट नं. 913) यासी क्षेत्र 00 हे 16 आर, गट नं. 913 (जुना गट नं. 914) यासी क्षेत्र 00 हे 19 आर, गट नं. 924 (जुना गट नं. 925) यासी क्षेत्र 00 हे 26.43 आर असे एकूण क्षेत्र 01 हे 2.43 आर या मिळकतीवर बांधलेल्या ऑक्सी अल्टीमा गृहप्रकल्पामधील ऑक्सी अल्टीमा सहकारी गृहरचना संस्था मर्या मधील विंग ए मधील चौथ्या मजल्यावरील फ्लॅट नं. A-406 यांसी क्षेत्र 483 चौ.फुट म्हणजेच 44.89 चौ.मी. कार्पेट + टेरेस क्षेत्र 98 चौ.फुट म्हणजेच 9.11 चौ.मी. तसेच कार पार्किंग CP-07 सह (( GAT NUMBER : 910 ))"
        },
        {
            "Document id": "Document 7",
            "url": "https://drive.google.com/file/d/17Gckl08aGD9psDz8xUmMg65j-xUJvVKK/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "28731/2025",
            "Seller/देनारा": ["वासुदेव गोविंद सोनकोळी"],
            "Buyer/घेणारा": ["विक्रम वासुदेव सोनकोळी"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे म.न.पा. इतर वर्णन, इतर माहिती: गाव मौजे बोपोडी येथील सिटीएस नं. 502 या मिळकतीवर बांधलेल्या रघुनाथ को-ऑप. हौसिंग सोसायटी लि. मधील विंग ए मधील तिसऱ्या मजल्यावरील फ्लॅट नं. 11 यांसी क्षेत्र 42.29 चौ.मी. (( C.T.S. Number : 502 ))"
        },
        {
            "Document id": "Document 8",
            "url": "https://drive.google.com/file/d/15fqPdsrFpV2L8Qnxzk8BUGRU052sNkwy/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "25625/2025",
            "Seller/देनारा": ["सुजाता कन्नन", "कन्नन रामामनी"],
            "Buyer/घेणारा": ["रीना बिनेश"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे म.न.पा. इतर वर्णन, इतर माहिती: गाव मौजे औंध येथील सि.स. नं. 2560 मधील प्रिझम को-ऑप हौसिंग सोसायटी लि. इमारत नं. बी-3 मधील तिसऱ्या मजल्यावरील फ्लॅट नं. 302 यांसी क्षेत्र 1039 चौ.फुट बिल्टअप सोबत जोडून टेरेस क्षेत्र 263 चौ.फुट तसेच तळमजल्यावरील कार पार्किंग नं. SC-242 (( C.T.S. Number : 2560 ))"
        },
        {
            "Document id": "Document 9",
            "url": "https://drive.google.com/file/d/1Dfert648Jj3mBycbla1dy7f6lfm6Qgat/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "33004/2024",
            "Seller/देनारा": ["माधवी रवींद्र माळी (लग्नापूर्वीचे नाव माधवी नयन कानेकर)"],
            "Buyer/घेणारा": ["कौस्तुभ किशोर वोरोले"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे म.न.पा. इतर वर्णन, इतर माहिती: बाणेर येथील सर्वे नं. 149/2/2/2, 149/2/1aft, 149/3/2, 148/1+2, 149/3/1, 149/2/2/1 इत्यादी मिळकतीवरील ग्रीन थंब अपार्टमेंट कंडोमिनियम मधील बिल्डिंग ए मधील चौथ्या मजल्यावरील फ्लॅट नं. A-110 क्षेत्र 1430 चौ.फुट / 132.85 चौ.मी. बांधीव टेरेस सह व तळमजल्यावरील एक पार्किंग तसेच जमिनीतील 3.71% अविभक्त हिस्सा (( Survey Number : 149 ))"
        },
        {
            "Document id": "Document 10",
            "url": "https://drive.google.com/file/d/17dnnlefT2phi8Wx4LZi6mP1mTzvxyx-q/view?usp=sharing",
            "Document_number/ दस्त क्रमांक": "27020/2025",
            "Seller/देनारा": ["अभिषेक गोयल", "बिदिशा भाणावत"],
            "Buyer/घेणारा": ["जिनीत संजय भारंबे", "नेहा जिनीत भारंबे"],
            "property_address_with_gat_numbers/ पत्ता": "पालिकेचे नाव: पुणे म.न.पा. इतर वर्णन, इतर माहिती: गाव मौजे बालेवाडी येथील सर्वे नं. 11/8/1 व 11/8/2 या मिळकतीवर बांधलेल्या ला विदा प्रोजेक्ट मधील विंग वी मधील अठराव्या मजल्यावरील फ्लॅट नं. 1805 यांसी कार्पेट क्षेत्र 88.74 चौ.मी. म्हणजेच 955.19 चौ.फुट तसेच लगतचे बाल्कनी क्षेत्र 14.53 चौ.मी. व एक कव्हर्ड पार्किंग"
        }
    ],
    'NOC': [
        {"Document id": "Document 1", "url": "https://drive.google.com/file/d/1t-ZyLYPaWI_UlYa-IqrvrtjXXixLPFE1/view?usp=sharing", "Name": ["Priya Tomar"], "Flat No": "305", "Address": "Konark Oasis Co-Operative Housing Society Limited, A Building, Wagholi, Pune 412207"},
        {"Document id": "Document 2", "url": "https://drive.google.com/file/d/1YZDMT9zAoi9qB1iKdXzDZ7pThUgZftxy/view?usp=sharing", "Name": ["ManojKumar B Solanki", "Mrs. Sejal Santosh Balkate"], "Flat No": "E1001", "Address": "Ayaan Co-operative Housing Society, Plot No.3,4,5 Wagholi, Tal. Haveli, Dist. Pune 412207"},
        {"Document id": "Document 3", "url": "https://drive.google.com/file/d/1qPD5FHNfA99qElJiJz5I6jhvPKcA1yB_/view?usp=sharing", "Name": ["Mr. Kishor Prabhakar Tarawade."], "Flat No": "B4-904", "Address": "Nyati Elan (South East) Co-operative Housing Society Ltd., Gat No. 720, 721, 723, 730 (Part) & 733, Wagholi, Tal. - Haveli, Dist. Pune, Pin.- 412 207."},
        {"Document id": "Document 4", "url": "https://drive.google.com/file/d/1smeo4NcRtSuFQoMsZlLFc05kxxYC-V55/view?usp=sharing", "Name": ["Mr. Mayur Digambar Pokale", "Mrs. Gauri Mayur Pokale"], "Flat No": "A1-1105", "Address": "B.A.Iris co-op. Hsg society, Chandannagar, Pune - 411014"},
        {"Document id": "Document 5", "url": "https://drive.google.com/file/d/1DR0rBHFnvosT11g678ONMTXOpYqgyJXx/view?usp=sharing", "Name": ["Mr. Sudarshan Rangnath Diwate", "Mrs. Jyoti Sudarshan Diwate"], "Flat No": "B2-805", "Address": "BA IRIS CO-Operative Housing Society Ltd., Chandannagar, Pune - 411014"},
        {"Document id": "Document 6", "url": "https://drive.google.com/file/d/1gpYMU2We4IkXc9jml7TYi-FC_J-uUp-z/view?usp=sharing", "Name": ["Smita S. Chavan"], "Flat No": "502", "Address": "St. Luke Co-operative Housing Society, 1, Guruvar Peth, Panch Haud, Pune - 411 042"},
        {"Document id": "Document 7", "url": "https://drive.google.com/file/d/13MkYDa3SnsUTyME2-KpOauJJpPezWFiJ/view?usp=sharing", "Name": ["VIKRAM VASUDEV SONKOLI"], "Flat No": "11", "Address": "RAGHUNATH CO OP HSG SOCIETY LTD, BLDG NO A, CTS NO.502, BOPODI, PUNE- 411020"},
        {"Document id": "Document 8", "url": "https://drive.google.com/file/d/136g1vwSQO1TaCgP5SK4AvKQssubTbiFC/view?usp=sharing", "Name": ["Mr. Bharat Balasaheb Jagdale", "Mrs. Seema Bharat Jagdale"], "Flat No": "B26", "Address": "मयुरी गार्डन सहकारी गृहरचना संस्था मर्यादित गट नंबर ११७३, वाघोली, तालुका- हवेली, जिल्हा पुणे"},
        {"Document id": "Document 9", "url": "https://drive.google.com/file/d/1aoBJwLIQ1dk1PSb-5t8wc23KH2NH-l5Z/view?usp=sharing", "Name": ["PRASHANT CHANDRA CHHOTELAL AGARWAL", "SANTOSH AGARWAL"], "Flat No": "B-404", "Address": "Army Welfare Housing Organization Near HQ Dakshin Maharashtra & Goa Sub Area Jijamata Road, Pune Camp"},
        {"Document id": "Document 10", "url": "https://drive.google.com/file/d/1__v9NYSupLna3xhxYHWh0VRERDSErKv2/view?usp=sharing", "Name": ["Mrs.Monisha Jagdish Kumar"], "Flat No": "11", "Address": "flat no.11 , C, 472/D, Salisbury Park, Pune 411037 , Poornima Park Co-op. Hsg. Soc. Ltd."}
    ],
    'No Dues': [
        {"Document id": "Document 1", "url": "https://drive.google.com/file/d/12sh-R90yDvstGOdyQPe5oc5jEgE-S8Cr/view?usp=drive_link", "Name": ["MUQTAR NAZIR SHAIKH", "AYESHA MUQTAR SHAIKH"], "Address": "H.NO. 35688 GAT NO. 878 & 879 F-201 MICASAA SOCIETY KESNAND ROAD WAGHOLI PUNE 412207", "Amount": "3695"},
        {"Document id": "Document 2", "url": "https://drive.google.com/file/d/15kvb2GyxmJPdkOvoHTm57hXgXkyktGt-/view?usp=drive_link", "Name": ["AALAP AVINASHA PTVARDHAN"], "Address": "1ST FLOOR, FLAT NO.102, SR.NO 111, PART 1 TO 5+16+17+112, H.NO 7 TO 9+11, PLOT NO.14, SUTARWADI, PASHA, PUNE", "Amount": "9258"},
        {"Document id": "Document 3", "url": "https://drive.google.com/file/d/14y7CLLvEQrLsuUGsnFhHEDVJJyHPhQwn/view?usp=drive_link", "Name": ["COL RAJENDRA KHATTRI", "MRS. SUSHMITA KHATTRI"], "Address": "FLAT NO A-601 WING-A, 6TH FLOOR GAT NO 1454, HISSA NO 1+2 & GAT NO 1455 (P), VIJAY VIHAR (AWHO) CO-OP HSG SOC LTD, MORE VASTI ROAD, WAGHOLI GAON, PUNE 412207", "Amount": "16189"},
        {"Document id": "Document 4", "url": "https://drive.google.com/file/d/1Z53SJ8wHlPdN63LTn-2P8_3FdatXmBCH/view?usp=drive_link", "Name": ["GANESH KISANRAO KHATAL", "KISANRAO K. KHATAL"], "Address": "H.NO.07966 G-302 GAT NO. 1213, 1214, 1215 & 1216 SAVANAH SOC., BAIF ROAD, WAGHOLI, PUNE 412207", "Amount": "14729"},
        {"Document id": "Document 5", "url": "https://drive.google.com/file/d/1grwkoghl43c1tHc0MyC0yGE3jxrgmO0P/view?usp=drive_link", "Name": ["NARENDRA KUMAR DEWANGAN", "SHEWTA DEWANGAN"], "Address": "H.NO.18025 A-305 GAT NO. 927 PLOT NO. 1, KONARK OASIS, KESNAND ROAD, WAGHOLI, PUNE 412207", "Amount": "12295"},
        {"Document id": "Document 6", "url": "https://drive.google.com/file/d/10RICEiTLwGFJnnDkH5QgroOXfWd-A7pS/view?usp=drive_link", "Name": ["SHIVSHANKAR PANCHAGALI"], "Address": "H.NO.15524 B4-904 NYATI ELAN B4, BAKORI ROAD, GAT NO 720, 721, 723, 733 & 730, WAGHOLI, PUNE 412207", "Amount": "12182"},
        {"Document id": "Document 7", "url": "https://drive.google.com/file/d/1kpwAERisacd4nUbSypJhnxTEvCq6_PGl/view?usp=drive_link", "Name": ["CHANDRASHEKHAR LAXMANRAO KALASKAR", "PALLAVI BIDKAR"], "Address": "H.NO.08351 C-508 UMANG PRIMO, C IVY ESTATE, GAT NO 690 TO 710, WAGHOLI, PUNE 412207", "Amount": "5659"},
        {"Document id": "Document 8", "url": "https://drive.google.com/file/d/1gBLzsNGuTz2QWDw4mvzAMX8o8FgfGkZY/view?usp=drive_link", "Name": ["SHRI. RAMESH ANANDRAO KADAM"], "Address": "O/6, 1ST FLOOR, H NO 721/1, GURUWAR PETH, PUNE 411002", "Amount": "4448"},
        {"Document id": "Document 9", "url": "https://drive.google.com/file/d/1hX01yLlPfj7IgLeUAok5ktiP2CArEWsB/view?usp=drive_link", "Name": ["SUGUNA CHANDRASEKARAN"], "Address": "FLAT NO 3, H NO 210/1, RASTA PETH, PUNE 411011", "Amount": "2891"},
        {"Document id": "Document 10", "url": "https://drive.google.com/file/d/1lwClKw0YdJUvC_imi0_Y3YMkLEf6OCsJ/view?usp=drive_link", "Name": ["PARANJAPE SUDHIR CHANDRAKANT"], "Address": "1ST FLOOR, FLAT NO.3+4, S.N. 425, PLOT NO.53, T.M.V. COLONY, GULTEKADI, PUNE 411043", "Amount": "5516"}
    ]
};

let documentCounter = 0;
const documents = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Debug: Log available data
    console.log('ACTUAL_DATA loaded:', Object.keys(ACTUAL_DATA).map(k => `${k}: ${ACTUAL_DATA[k].length} docs`));
    
    // Auto-detect API URL from current page URL
    const apiUrlInput = document.getElementById('apiUrl');
    if (apiUrlInput) {
        // Get current origin (protocol + host + port)
        const currentOrigin = window.location.origin;
        // Always set both value and placeholder to ensure it's available
        if (!apiUrlInput.value || apiUrlInput.value.trim() === '') {
            apiUrlInput.value = currentOrigin;
        }
        if (!apiUrlInput.placeholder || apiUrlInput.placeholder.trim() === '') {
            apiUrlInput.placeholder = currentOrigin;
        }
    }
    
    document.getElementById('addDocumentBtn').addEventListener('click', addDocument);
    document.getElementById('submitBtn').addEventListener('click', submitDocuments);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    document.getElementById('processManualResultsBtn').addEventListener('click', processManualResults);
    
    // Show/hide test mode section based on checkbox
    const testModeCheckbox = document.getElementById('testMode');
    const testModeSection = document.getElementById('testModeSection');
    testModeCheckbox.addEventListener('change', () => {
        if (testModeCheckbox.checked) {
            testModeSection.classList.remove('hidden');
        } else {
            testModeSection.classList.add('hidden');
        }
    });
    
    // Initialize test mode section visibility
    if (testModeCheckbox.checked) {
        testModeSection.classList.remove('hidden');
    }
});

function addDocument() {
    documentCounter++;
    const docId = `doc-${documentCounter}`;
    
    const docCard = document.createElement('div');
    docCard.className = 'document-card';
    docCard.id = docId;
    
    docCard.innerHTML = `
        <div class="document-card-header">
            <h3>Document #${documentCounter}</h3>
            <button class="btn btn-danger" onclick="removeDocument('${docId}')">Remove</button>
        </div>
        <div class="form-group">
            <label>Document Type:</label>
            <select class="doc-type-select" onchange="updateDocumentFields('${docId}', this.value)">
                <option value="">Select Document Type</option>
                <option value="Index 2">Index 2</option>
                <option value="NOC">NOC</option>
                <option value="No Dues">No Dues</option>
            </select>
        </div>
        <div class="form-group doc-selector-group" style="display: none;">
            <label>Select Document (for auto-fill):</label>
            <select class="doc-selector" onchange="selectDocument('${docId}', this.value)">
                <option value="">Select a document...</option>
            </select>
            <small style="color: var(--text-secondary); font-size: 0.85rem; display: block; margin-top: 5px;">
                💡 Choose a pre-filled document or select "Other" to fill manually
            </small>
        </div>
        <div class="form-group">
            <label>Download URL:</label>
            <input type="url" class="doc-url-input" placeholder="https://pmc.gov.in/uploads/doc.pdf or Google Drive link">
            <small style="color: var(--text-secondary); font-size: 0.85rem; display: block; margin-top: 5px;">
                💡 Supports direct URLs and Google Drive sharing links (automatically converted)
            </small>
        </div>
        <div class="doc-fields-container"></div>
    `;
    
    document.getElementById('documentsContainer').appendChild(docCard);
    documents.push({ id: docId, type: null, url: '', fields: {} });
    
    // Add event listener for URL input
    const urlInput = docCard.querySelector('.doc-url-input');
    if (urlInput) {
        urlInput.addEventListener('input', () => updateDocumentData(docId));
    }
    
    // Add event listeners for required fields to update submit button
    const bearerTokenInput = document.getElementById('bearerToken');
    const appNoInput = document.getElementById('appNo');
    if (bearerTokenInput) {
        bearerTokenInput.addEventListener('input', updateSubmitButton);
    }
    if (appNoInput) {
        appNoInput.addEventListener('input', updateSubmitButton);
    }
    
    updateSubmitButton();
}

function removeDocument(docId) {
    const docCard = document.getElementById(docId);
    if (docCard) {
        docCard.remove();
        const index = documents.findIndex(d => d.id === docId);
        if (index > -1) {
            documents.splice(index, 1);
        }
        updateSubmitButton();
    }
}

function updateDocumentFields(docId, docType) {
    const docCard = document.getElementById(docId);
    const fieldsContainer = docCard.querySelector('.doc-fields-container');
    const docSelectorGroup = docCard.querySelector('.doc-selector-group');
    const docSelector = docCard.querySelector('.doc-selector');
    const docIndex = documents.findIndex(d => d.id === docId);
    
    if (docIndex === -1) return;
    
    documents[docIndex].type = docType;
    fieldsContainer.innerHTML = '';
    
    // Show/hide document selector based on document type
    if (docType && DOCUMENT_TYPES[docType]) {
        // Show document selector and populate it
        docSelectorGroup.style.display = 'block';
        populateDocumentSelector(docId, docType);
    } else {
        docSelectorGroup.style.display = 'none';
        updateSubmitButton();
        return;
    }
    
    const fields = DOCUMENT_TYPES[docType].fields;
    
    fields.forEach(field => {
        const fieldGroup = document.createElement('div');
        fieldGroup.className = 'form-group';
        
        if (field.isArray) {
            fieldGroup.className += ' array-field-group';
            fieldGroup.innerHTML = `
                <label>${field.name}:</label>
                <div class="array-items-container" data-field="${field.name}">
                    <div class="array-item">
                        <input type="${field.type === 'textarea' ? 'text' : field.type}" 
                               class="array-field-input" 
                               data-field="${field.name}" 
                               placeholder="Enter ${field.name}">
                        <button type="button" class="btn btn-danger" onclick="removeArrayItem(this)">Remove</button>
                    </div>
                </div>
                <button type="button" class="add-item-btn" onclick="addArrayItem('${docId}', '${field.name}', '${field.type}')">+ Add ${field.name}</button>
            `;
        } else {
            if (field.type === 'textarea') {
                fieldGroup.innerHTML = `
                    <label>${field.name}:</label>
                    <textarea class="doc-field-input" data-field="${field.name}" placeholder="Enter ${field.name}"></textarea>
                `;
            } else {
                fieldGroup.innerHTML = `
                    <label>${field.name}:</label>
                    <input type="${field.type}" class="doc-field-input" data-field="${field.name}" placeholder="Enter ${field.name}">
                `;
            }
        }
        
        fieldsContainer.appendChild(fieldGroup);
    });
    
    // Initialize fields in documents array
    documents[docIndex].fields = {};
    fields.forEach(field => {
        if (field.isArray) {
            documents[docIndex].fields[field.name] = [''];
        } else {
            documents[docIndex].fields[field.name] = '';
        }
    });
    
    // Add event listeners for field changes
    fieldsContainer.querySelectorAll('.doc-field-input, .array-field-input').forEach(input => {
        input.addEventListener('input', () => updateDocumentData(docId));
    });
    
    updateSubmitButton();
}

function populateDocumentSelector(docId, docType) {
    const docCard = document.getElementById(docId);
    const docSelector = docCard.querySelector('.doc-selector');
    
    if (!docSelector) {
        console.warn('Document selector not found for', docId);
        return;
    }
    
    // Clear existing options
    docSelector.innerHTML = '<option value="">Select a document...</option>';
    
    // Get available documents for this type
    const availableDocs = ACTUAL_DATA[docType] || [];
    
    console.log('Populating selector for type:', docType, 'Found', availableDocs.length, 'documents');
    
    if (availableDocs.length > 0) {
        // Add document options
        availableDocs.forEach((doc, index) => {
            const option = document.createElement('option');
            const docIdValue = doc['Document id'] || `Document ${index + 1}`;
            option.value = docIdValue;
            option.textContent = docIdValue;
            docSelector.appendChild(option);
        });
        
        // Add "Other" option
        const otherOption = document.createElement('option');
        otherOption.value = 'Other';
        otherOption.textContent = 'Other (Fill manually)';
        docSelector.appendChild(otherOption);
    } else {
        console.warn('No documents found for type:', docType);
        // No pre-filled data available, show only "Other"
        const otherOption = document.createElement('option');
        otherOption.value = 'Other';
        otherOption.textContent = 'Other (Fill manually)';
        docSelector.appendChild(otherOption);
    }
}

function selectDocument(docId, selectedDocId) {
    const docCard = document.getElementById(docId);
    const docIndex = documents.findIndex(d => d.id === docId);
    
    if (docIndex === -1) return;
    
    const docType = documents[docIndex].type;
    
    if (!docType || selectedDocId === '' || selectedDocId === 'Other') {
        // Clear auto-filled data if "Other" is selected or empty
        if (selectedDocId === 'Other') {
            clearAutoFilledData(docId);
        }
        updateSubmitButton();
        return;
    }
    
    // Find the selected document data
    const availableDocs = ACTUAL_DATA[docType] || [];
    const selectedDoc = availableDocs.find(doc => doc['Document id'] === selectedDocId);
    
    if (!selectedDoc) {
        console.warn('Selected document not found:', selectedDocId);
        return;
    }
    
    // Auto-fill URL
    const urlInput = docCard.querySelector('.doc-url-input');
    if (urlInput && selectedDoc.url) {
        urlInput.value = selectedDoc.url;
    }
    
    // Auto-fill fields
    const fields = DOCUMENT_TYPES[docType].fields;
    fields.forEach(field => {
        const fieldName = field.name;
        // Try to find field value with case-insensitive matching
        let fieldValue = selectedDoc[fieldName];
        
        // If not found, try case-insensitive search
        if (fieldValue === undefined || fieldValue === null) {
            const keys = Object.keys(selectedDoc);
            const matchingKey = keys.find(key => 
                key.toLowerCase() === fieldName.toLowerCase() ||
                key.toLowerCase().replace(/\s+/g, ' ') === fieldName.toLowerCase().replace(/\s+/g, ' ')
            );
            if (matchingKey) {
                fieldValue = selectedDoc[matchingKey];
            }
        }
        
        if (fieldValue !== undefined && fieldValue !== null) {
            if (field.isArray) {
                // Handle array fields
                const container = docCard.querySelector(`[data-field="${fieldName}"]`);
                if (container) {
                    // Clear existing items
                    container.innerHTML = '';
                    
                    // Add items from data
                    const values = Array.isArray(fieldValue) ? fieldValue : [fieldValue];
                    values.forEach((value, index) => {
                        const arrayItem = document.createElement('div');
                        arrayItem.className = 'array-item';
                        arrayItem.innerHTML = `
                            <input type="${field.type === 'textarea' ? 'text' : field.type}" 
                                   class="array-field-input" 
                                   data-field="${fieldName}" 
                                   value="${escapeHtml(String(value))}"
                                   placeholder="Enter ${fieldName}">
                            <button type="button" class="btn btn-danger" onclick="removeArrayItem(this)">Remove</button>
                        `;
                        container.appendChild(arrayItem);
                        
                        // Add event listener
                        arrayItem.querySelector('input').addEventListener('input', () => updateDocumentData(docId));
                    });
                    
                    // Add "Add" button if not exists
                    const addBtn = docCard.querySelector(`.add-item-btn[onclick*="${fieldName}"]`);
                    if (!addBtn) {
                        const addButton = document.createElement('button');
                        addButton.type = 'button';
                        addButton.className = 'add-item-btn';
                        addButton.textContent = `+ Add ${fieldName}`;
                        addButton.onclick = () => addArrayItem(docId, fieldName, field.type);
                        container.parentElement.appendChild(addButton);
                    }
                }
            } else {
                // Handle single fields
                const input = docCard.querySelector(`.doc-field-input[data-field="${fieldName}"]`);
                if (input) {
                    if (field.type === 'textarea') {
                        input.value = String(fieldValue);
                    } else {
                        input.value = String(fieldValue);
                    }
                }
            }
        }
    });
    
    // Update document data
    updateDocumentData(docId);
    updateSubmitButton();
}

function clearAutoFilledData(docId) {
    const docCard = document.getElementById(docId);
    
    // Clear URL
    const urlInput = docCard.querySelector('.doc-url-input');
    if (urlInput) {
        urlInput.value = '';
    }
    
    // Clear all field inputs
    const docIndex = documents.findIndex(d => d.id === docId);
    if (docIndex === -1) return;
    
    const docType = documents[docIndex].type;
    if (!docType) return;
    
    const fields = DOCUMENT_TYPES[docType].fields;
    fields.forEach(field => {
        const fieldName = field.name;
        if (field.isArray) {
            const container = docCard.querySelector(`[data-field="${fieldName}"]`);
            if (container) {
                // Keep only one empty item
                container.innerHTML = '';
                const arrayItem = document.createElement('div');
                arrayItem.className = 'array-item';
                arrayItem.innerHTML = `
                    <input type="${field.type === 'textarea' ? 'text' : field.type}" 
                           class="array-field-input" 
                           data-field="${fieldName}" 
                           placeholder="Enter ${fieldName}">
                    <button type="button" class="btn btn-danger" onclick="removeArrayItem(this)">Remove</button>
                `;
                container.appendChild(arrayItem);
                arrayItem.querySelector('input').addEventListener('input', () => updateDocumentData(docId));
            }
        } else {
            const input = docCard.querySelector(`.doc-field-input[data-field="${fieldName}"]`);
            if (input) {
                input.value = '';
            }
        }
    });
    
    updateDocumentData(docId);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function addArrayItem(docId, fieldName, fieldType) {
    const docCard = document.getElementById(docId);
    const container = docCard.querySelector(`[data-field="${fieldName}"]`);
    
    const arrayItem = document.createElement('div');
    arrayItem.className = 'array-item';
    arrayItem.innerHTML = `
        <input type="${fieldType === 'textarea' ? 'text' : fieldType}" 
               class="array-field-input" 
               data-field="${fieldName}" 
               placeholder="Enter ${fieldName}">
        <button type="button" class="btn btn-danger" onclick="removeArrayItem(this)">Remove</button>
    `;
    
    container.appendChild(arrayItem);
    
    // Add event listener
    arrayItem.querySelector('input').addEventListener('input', () => updateDocumentData(docId));
    
    updateDocumentData(docId);
}

function removeArrayItem(button) {
    const container = button.closest('.array-items-container');
    if (container && container.children.length > 1) {
        button.closest('.array-item').remove();
        const docId = button.closest('.document-card').id;
        updateDocumentData(docId);
    } else {
        alert('At least one item is required for this field.');
    }
}

function updateDocumentData(docId) {
    const docCard = document.getElementById(docId);
    const docIndex = documents.findIndex(d => d.id === docId);
    
    if (docIndex === -1) return;
    
    // Update URL
    const urlInput = docCard.querySelector('.doc-url-input');
    documents[docIndex].url = urlInput ? urlInput.value : '';
    
    // Update fields
    const fields = DOCUMENT_TYPES[documents[docIndex].type]?.fields || [];
    
    fields.forEach(field => {
        if (field.isArray) {
            const inputs = docCard.querySelectorAll(`.array-field-input[data-field="${field.name}"]`);
            documents[docIndex].fields[field.name] = Array.from(inputs).map(input => input.value).filter(v => v.trim() !== '');
        } else {
            const input = docCard.querySelector(`.doc-field-input[data-field="${field.name}"]`);
            documents[docIndex].fields[field.name] = input ? input.value : '';
        }
    });
    
    updateSubmitButton();
}

function updateSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    const bearerToken = document.getElementById('bearerToken')?.value.trim() || '';
    const appNo = document.getElementById('appNo')?.value.trim() || '';
    const hasValidDocuments = documents.some(doc => 
        doc.type && 
        doc.url && 
        doc.url.trim() !== '' &&
        Object.values(doc.fields).some(val => 
            Array.isArray(val) ? val.length > 0 && val.some(v => v.trim() !== '') : val.trim() !== ''
        )
    );
    
    // Disable if missing required fields or no valid documents
    submitBtn.disabled = !hasValidDocuments || !bearerToken || !appNo;
}

function clearAll() {
    if (confirm('Are you sure you want to clear all documents?')) {
        document.getElementById('documentsContainer').innerHTML = '';
        documents.length = 0;
        documentCounter = 0;
        document.getElementById('resultsSection').classList.add('hidden');
        document.getElementById('errorSection').classList.add('hidden');
        updateSubmitButton();
    }
}

async function submitDocuments() {
    const apiUrlInput = document.getElementById('apiUrl');
    let apiUrl = apiUrlInput.value.trim();
    
    // If empty, try to use placeholder or auto-detect
    if (!apiUrl) {
        apiUrl = apiUrlInput.placeholder.trim() || window.location.origin;
        if (apiUrl) {
            apiUrlInput.value = apiUrl;
        }
    }
    
    if (!apiUrl) {
        showError('Please provide an API URL');
        return;
    }
    
    // Validate Bearer token (required for new system)
    const bearerTokenInput = document.getElementById('bearerToken');
    const bearerToken = bearerTokenInput ? bearerTokenInput.value.trim() : '';
    if (!bearerToken) {
        showError('Bearer Token is required. Please enter your Bearer token in the configuration section.');
        return;
    }
    
    // Validate appNo (required for new system)
    const appNoInput = document.getElementById('appNo');
    const appNo = appNoInput ? appNoInput.value.trim() : '';
    if (!appNo) {
        showError('Application Number (appNo) is required. Please enter an application number.');
        return;
    }
    
    // Validate all documents
    const validDocuments = documents.filter(doc => 
        doc.type && 
        doc.url && 
        doc.url.trim() !== '' &&
        Object.values(doc.fields).some(val => 
            Array.isArray(val) ? val.length > 0 && val.some(v => v.trim() !== '') : val.trim() !== ''
        )
    );
    
    if (validDocuments.length === 0) {
        showError('Please add at least one valid document with all required fields filled.');
        return;
    }
    
    // Build request payload (updated for new system)
    const payload = {
        service_name: 'PT5',
        appNo: appNo,
        documents: validDocuments.map(doc => {
            // Ensure array fields are arrays (not empty arrays if they have no values)
            const actualData = { ...doc.fields };
            const docTypeConfig = DOCUMENT_TYPES[doc.type];
            if (docTypeConfig) {
                docTypeConfig.fields.forEach(field => {
                    if (field.isArray) {
                        // Ensure it's an array and has at least one value
                        if (!Array.isArray(actualData[field.name]) || actualData[field.name].length === 0) {
                            // This shouldn't happen due to validation, but handle it gracefully
                            actualData[field.name] = actualData[field.name] || [];
                        }
                    }
                });
            }
            return {
                download_url: doc.url,
                document_type: doc.type,
                actual_data: actualData
            };
        })
    };
    
    // Show loading
    document.getElementById('loadingSection').classList.remove('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('errorSection').classList.add('hidden');
    document.getElementById('submitBtn').disabled = true;
    
    // Get API token if provided (optional)
    const apiTokenInput = document.getElementById('apiToken');
    const apiToken = apiTokenInput ? apiTokenInput.value.trim() : '';
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${bearerToken}`  // Required for new system
    };
    
    // Add API token to headers if provided (optional)
    if (apiToken) {
        headers['X-API-Token'] = apiToken;
    }
    
    // Debug: Log what we're sending
    console.log('Sending request to:', `${apiUrl}/api/v1/verify`);
    console.log('Headers:', Object.keys(headers));
    console.log('Payload:', payload);
    
    try {
        const response = await fetch(`${apiUrl}/api/v1/verify`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });
        
        // Check if response is OK before parsing JSON
        if (!response.ok) {
            // Try to get error message from JSON response
            let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
            } catch (e) {
                // If response is not JSON, use status text
                const text = await response.text();
                if (text) {
                    errorMessage = text.substring(0, 200); // Limit length
                }
            }
            
            // Special handling for 401 (missing/invalid Bearer token)
            if (response.status === 401) {
                errorMessage = `Authentication Error: ${errorMessage}. Please check your Bearer token.`;
            }
            
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        
        // New system returns only acknowledgment, not full results
        // Results will come via webhook, but for local testing we show the acknowledgment
        if (data.success && data.service_name && data.appNo) {
            // This is the new async response format
            const testMode = document.getElementById('testMode').checked;
            if (testMode) {
                // Show test mode section for manual result entry
                showAcknowledgment(data);
                document.getElementById('testModeSection').classList.remove('hidden');
            } else {
                // Show acknowledgment message
                showAcknowledgment(data);
            }
        } else {
            // Old format or unexpected response - try to display as results
            displayResults(data);
        }
    } catch (error) {
        // Better error message handling
        let errorMsg = error.message;
        if (errorMsg === 'Failed to fetch') {
            errorMsg = 'Failed to connect to API. Please check:\n1. API is running at the URL shown\n2. Bearer token is correct (required)\n3. No CORS issues';
        }
        showError(`Error: ${errorMsg}`);
    } finally {
        document.getElementById('loadingSection').classList.add('hidden');
        document.getElementById('submitBtn').disabled = false;
        updateSubmitButton();
    }
}

function showAcknowledgment(data) {
    const resultsSection = document.getElementById('resultsSection');
    const summarySection = document.getElementById('summarySection');
    const detailedResults = document.getElementById('detailedResults');
    
    const taskId = data.task_id || 'N/A';
    const apiUrl = document.getElementById('apiUrl').value.trim();
    
    summarySection.innerHTML = `
        <div class="acknowledgment-card">
            <h3>✅ Request Accepted</h3>
            <p><strong>Service:</strong> ${data.service_name}</p>
            <p><strong>Application Number:</strong> ${data.appNo}</p>
            ${taskId !== 'N/A' ? `<p><strong>Task ID:</strong> <code style="background: var(--bg-color); padding: 2px 6px; border-radius: 3px; font-size: 0.9em;">${taskId}</code></p>` : ''}
            <p style="margin-top: 15px; color: var(--text-secondary);">
                Your request has been queued for processing. Results will be sent via webhook when processing completes.
            </p>
            ${taskId !== 'N/A' ? `
            <div style="margin-top: 15px; padding: 10px; background: var(--bg-color); border-radius: 6px;">
                <p style="margin: 0 0 10px 0; font-weight: 600;">For Local Testing:</p>
                <button onclick="checkTaskResult('${taskId}', '${apiUrl}')" class="btn" style="margin-right: 10px;">Check Results</button>
                <span style="color: var(--text-secondary); font-size: 0.9em;">or enable "Test Mode" to paste results manually</span>
            </div>
            ` : ''}
            <p style="margin-top: 10px; color: var(--text-secondary); font-size: 0.9em;">
                <strong>Note:</strong> For local testing, enable "Test Mode" and paste the webhook response JSON manually.
            </p>
        </div>
    `;
    
    detailedResults.innerHTML = '';
    resultsSection.classList.remove('hidden');
}

async function checkTaskResult(taskId, apiUrl) {
    if (!taskId || taskId === 'N/A') {
        showError('Task ID not available');
        return;
    }
    
    try {
        const bearerToken = document.getElementById('bearerToken')?.value.trim() || '';
        // Get API token if provided (same as submitDocuments)
        const apiTokenInput = document.getElementById('apiToken');
        const apiToken = apiTokenInput ? apiTokenInput.value.trim() : '';
        
        const headers = {
            'Authorization': `Bearer ${bearerToken}`,
            'Content-Type': 'application/json'
        };
        
        // Add API token to headers if provided (required for /api endpoints)
        if (apiToken) {
            headers['X-API-Token'] = apiToken;
        }
        
        const response = await fetch(`${apiUrl}/api/v1/task/${taskId}`, {
            method: 'GET',
            headers: headers
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'completed' && data.result) {
            // Display the results
            displayResults(data.result);
            // Hide test mode section if it was shown
            document.getElementById('testModeSection').classList.add('hidden');
        } else if (data.status === 'pending') {
            alert('Task is still being processed. Please wait a moment and try again.');
        } else if (data.status === 'failed') {
            showError(`Task failed: ${data.error || 'Unknown error'}`);
        } else {
            showError(`Unexpected response: ${JSON.stringify(data)}`);
        }
    } catch (error) {
        showError(`Error checking task result: ${error.message}`);
    }
}

function processManualResults() {
    const manualResultsText = document.getElementById('manualResults').value.trim();
    if (!manualResultsText) {
        showError('Please paste the webhook response JSON');
        return;
    }
    
    try {
        const data = JSON.parse(manualResultsText);
        displayResults(data);
        document.getElementById('testModeSection').classList.add('hidden');
    } catch (error) {
        showError(`Invalid JSON: ${error.message}`);
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const summarySection = document.getElementById('summarySection');
    const detailedResults = document.getElementById('detailedResults');
    
    // Debug: Log timing data
    console.log('Results data:', {
        total_processing_time: data.total_processing_time,
        results_count: data.results?.length,
        processing_times: data.results?.map(r => ({ type: r.document_type, time: r.processing_time }))
    });
    
    // Calculate total processing time (sum of all document times or use total_processing_time if available)
    let totalTime = data.total_processing_time;
    if (totalTime === undefined || totalTime === null || totalTime === 0) {
        if (data.results && data.results.length > 0) {
            totalTime = data.results.reduce((sum, r) => {
                const docTime = r.processing_time;
                const timeValue = docTime !== undefined && docTime !== null ? docTime : 0;
                return sum + timeValue;
            }, 0);
        } else {
            totalTime = 0;
        }
    }
    
    console.log('Calculated total time:', totalTime);
    
    // Display summary
    summarySection.innerHTML = `
        <div class="summary-card">
            <h4>Total Documents</h4>
            <div class="value">${data.total_documents || 0}</div>
        </div>
        <div class="summary-card">
            <h4>Successful</h4>
            <div class="value success">${data.successful || 0}</div>
        </div>
        <div class="summary-card">
            <h4>Failed</h4>
            <div class="value error">${data.failed || 0}</div>
        </div>
        <div class="summary-card">
            <h4>Average Accuracy</h4>
            <div class="value ${getAccuracyClass(data.average_accuracy)}">${formatAccuracy(data.average_accuracy)}</div>
        </div>
        <div class="summary-card">
            <h4>Total Processing Time</h4>
            <div class="value">${formatTime(totalTime)}</div>
        </div>
    `;
    
    // Display detailed results
    detailedResults.innerHTML = '';
    
    if (data.results && data.results.length > 0) {
        data.results.forEach((result, index) => {
            const resultCard = document.createElement('div');
            resultCard.className = 'document-result';
            
            const accuracyClass = getAccuracyClass(result.accuracy);
            const accuracyBadgeClass = getAccuracyBadgeClass(result.accuracy);
            
            // Get processing time for this document
            const docProcessingTime = result.processing_time !== undefined && result.processing_time !== null 
                ? result.processing_time 
                : null;
            
            resultCard.innerHTML = `
                <div class="document-result-header">
                    <div>
                        <span class="success-indicator ${result.success ? 'success' : 'failed'}"></span>
                        <strong>${result.document_type}</strong>
                    </div>
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                        <div class="accuracy-badge ${accuracyBadgeClass}">
                            ${formatAccuracy(result.accuracy)}
                        </div>
                        ${docProcessingTime !== null ? `
                            <div style="font-size: 0.95em; color: var(--text-secondary); font-weight: 500; padding: 4px 8px; background: var(--bg-color); border-radius: 4px;">
                                ⏱️ ${formatTime(docProcessingTime)}
                            </div>
                        ` : '<div style="font-size: 0.95em; color: var(--text-secondary); font-weight: 500; padding: 4px 8px;">⏱️ N/A</div>'}
                    </div>
                </div>
                <div class="form-group">
                    <label>Document URL:</label>
                    <a href="${result.document_url}" target="_blank" style="color: var(--primary-color); word-break: break-all;">${result.document_url}</a>
                </div>
                ${result.error ? `
                    <div class="error-section" style="margin-top: 15px;">
                        <strong>Error:</strong> ${result.error}
                    </div>
                ` : ''}
                ${result.fields_accuracy && Object.keys(result.fields_accuracy).length > 0 ? `
                    <h4 style="margin-top: 20px; margin-bottom: 15px;">Field Accuracy Details:</h4>
                    ${Object.entries(result.fields_accuracy).map(([fieldName, fieldData]) => {
                        const fieldAccClass = getAccuracyClass(fieldData.accuracy);
                        return `
                            <div class="field-accuracy ${fieldAccClass}">
                                <h5>${fieldName} - ${formatAccuracy(fieldData.accuracy)}</h5>
                                <div class="field-comparison">
                                    <div class="comparison-item">
                                        <label>Actual:</label>
                                        <div class="value">${escapeHtml(String(fieldData.actual || ''))}</div>
                                    </div>
                                    <div class="comparison-item">
                                        <label>Predicted:</label>
                                        <div class="value">${escapeHtml(String(fieldData.predicted || ''))}</div>
                                    </div>
                                </div>
                                ${fieldData.method ? `
                                    <div class="method-badge">
                                        Method: ${fieldData.method}${fieldData.details ? ` - ${fieldData.details}` : ''}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }).join('')}
                ` : ''}
                ${result.extracted_fields && Object.keys(result.extracted_fields).length > 0 ? `
                    <details style="margin-top: 20px;">
                        <summary style="cursor: pointer; font-weight: 600; margin-bottom: 10px;">Extracted Fields</summary>
                        <pre style="background: var(--bg-color); padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 0.9rem;">${JSON.stringify(result.extracted_fields, null, 2)}</pre>
                    </details>
                ` : ''}
            `;
            
            detailedResults.appendChild(resultCard);
        });
    }
    
    resultsSection.classList.remove('hidden');
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
}

function formatAccuracy(accuracy) {
    if (accuracy === null || accuracy === undefined) return 'N/A';
    return `${(accuracy * 100).toFixed(2)}%`;
}

function getAccuracyClass(accuracy) {
    if (accuracy === null || accuracy === undefined) return '';
    if (accuracy >= 0.9) return 'success';
    if (accuracy >= 0.7) return 'medium';
    return 'error';
}

function getAccuracyBadgeClass(accuracy) {
    if (accuracy === null || accuracy === undefined) return '';
    if (accuracy >= 0.9) return 'high';
    if (accuracy >= 0.7) return 'medium';
    return 'low';
}

function formatTime(seconds) {
    if (seconds === null || seconds === undefined) return 'N/A';
    if (seconds === 0) return '0.00s';
    
    if (seconds < 1) {
        return `${(seconds * 1000).toFixed(0)}ms`;
    } else if (seconds < 60) {
        return `${seconds.toFixed(2)}s`;
    } else {
        const mins = Math.floor(seconds / 60);
        const secs = (seconds % 60).toFixed(2);
        return `${mins}m ${secs}s`;
    }
}
