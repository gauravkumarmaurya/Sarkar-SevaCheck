Sarkar SevaCheck - Synthetic OCR Test Receipts
=================================================

IMPORTANT: Every image in this folder is synthetic/demo data and is NOT an official government receipt.

20 service examples are included, one per service.

Verified-fee overcharge tests:
- Caste Certificate: demo receipt total ₹150; current verified fee record is ₹40.
- Employment Registration: demo receipt total ₹80; current verified fee record is ₹40.

Unverified-service tests:
The other 18 services currently do not have a verified fee record in the demo database, so the app should NOT declare their charges valid/invalid based on an unverified fee.

Suggested test:
1. Open Scan Receipt.
2. Select the service.
3. Upload the matching PNG.
4. Run OCR.
5. Check the extracted total amount.
6. For Caste Certificate / Employment Registration, test the comparison/report flow.
7. For other services, confirm the app shows that a verified fee record is not available.
