Explanation:
name and name_arb: These fields capture the name of the entity in English and Arabic.
ABBR: This is an abbreviation for the entity.
entity_type: Indicates whether the entity is "internal" or "external".
contacts: An array of objects, each representing a contact with fields for name, email, and phone number.
ports: An array of objects where each object represents a port used by the entity. Each port object includes:
number: The port number.
service_access: A boolean indicating if the service is accessible.
allowed_access: An array of IPs allowed access to the port.
certificates and consumer_certificates: Arrays of certificate objects, each detailing a certificate's name and its expiry date.
user_accounts: An array of user account objects, each detailing the user's name, roles, and associated certificates.
This JSON structure provides a comprehensive overview of the entity, including detailed information about its contacts, ports, and user accounts. Adjust the values and add more items as needed to fit the specific use case.

The entity object contains the following properties:

name: The name of the entity.
name_arb: The Arabic name of the entity.
ABBR: The abbreviation of the entity.
entityType: The type of the entity, which can be "internal" or "external".
contacts: An array of contact objects, each containing:
name: The name of the contact person.
email: The email address of the contact person.
phoneNumber: The phone number of the contact person.
ports: An array of port objects, each containing:
number: The port number.
serviceAccess: The service access type (e.g., "http", "https").
allowedAccess: An array of allowed access methods for the port.
certificates: An array of certificate objects associated with the port, each containing:
name: The name of the certificate.
expiryDate: The expiry date of the certificate.
consumerCertificates: An array of consumer certificate objects, each containing:
name: The name of the consumer certificate.
expiryDate: The expiry date of the consumer certificate.
userAccounts: An array of user account objects, each containing:
name: The name of the user account.
roles: An array of roles assigned to the user account.
certificates: An array of certificate objects associated with the user account, each containing:
name: The name of the certificate.
expiryDate: The expiry date of the certificate.