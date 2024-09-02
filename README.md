# REX: Seamless Django Database Transformation and Migration (Sender)

Effortlessly migrate and synchronize data between Django projects across servers and databases, with enhanced security and real-time communication.

## 🚀 Introduction

REX is a powerful tool designed to facilitate seamless data migration between Django projects, whether on the same or different servers, supporting cross-database transfers between PostgreSQL, SQL, and more. This README is specifically for the **sender** part of the REX project, which is responsible for initiating the migration process. REX handles the complexity of synchronizing both the database schema and the data itself, ensuring a smooth transition, even between different database systems. With built-in encryption and real-time communication via WebSockets, REX offers a secure and reliable solution for data transfer.

## ✨ Key Features

- **Cross-Database Migration**: Effortlessly transfer data between Django projects, even when using different database systems (e.g., PostgreSQL to SQL). REX ensures compatibility by transforming data into Django native fields.
- **End-to-End Encryption**: Protect your data with secure encryption during every step of the migration process. REX uses private and public keys for secure synchronization, ensuring only authorized projects can connect and share data.
- **Real-Time Communication**: Using WebSockets, REX provides real-time feedback on the migration process, from schema verification to data synchronization, allowing you to track progress dynamically.
- **Schema Validation**: Before data migration begins, REX ensures that the schemas between the source and destination databases are compatible. It thoroughly checks model fields and relationships to ensure data integrity.
- **Transaction Management**: REX performs the entire migration inside a transaction, allowing for a rollback in case of errors or connection issues, ensuring your data is always safe.

## 🛠 Installation

Before getting started, install the necessary dependencies:

```bash
bashCopy code
pip install -r requirements.txt

```

Ensure that Redis is installed and running, as it is required for WebSocket communication:

```bash
bashCopy code
brew install redis

```

## 🔧 Configuration

In your `.env` file, configure the following settings:

```bash
bashCopy code
REDIS_PORT=redis://127.0.0.1:6379
SECRET_KEY=your-django-secret-key
DATA_SYNC_RECEIVER_TOKEN=your-unique-receiver-token

```

Ensure both the sender and receiver projects have matching `DATA_SYNC_RECEIVER_TOKEN` and `SECRET_KEY` values.

Settings Example:

```python
pythonCopy code
INSTALLED_APPS = [
    "daphne",
    'corsheaders',
    'django_data_seed',
    # other apps
]

```

## ⚙️ How It Works

1. **Token and Key Validation**: The sender and receiver servers exchange tokens (defined in `.env`). If the tokens match, the connection is established. Once the tokens are verified, both servers validate their `SECRET_KEY` settings to confirm compatibility.
2. **Schema Validation**: The sender server receives the schema from the receiver and validates each model and field. All schema properties are encrypted before transmission, ensuring data security.
3. **Data Synchronization**: Upon successful schema validation, the sender server dumps the data into JSON format. The data is transferred incrementally, with each instance encrypted before being sent to the receiver.
4. **Progress Tracking**: The sender server provides a real-time update on the data transfer progress, reducing the total count as the transfer progresses. The process continues until all data is successfully synchronized.
5. **Completion**: Once data synchronization is complete, the receiver server confirms the success, and the transaction is committed.

## 🎛 Web Interface

- **Connection Establishment**: View real-time messages as the sender and receiver establish communication.
- **Schema Validation**: Get live feedback during schema verification.
- **Data Transfer**: Monitor the percentage of data transferred and track the overall progress.

## 🧩 Packages Used

- `channels==4.1.0`
- `channels-redis==4.2.0`
- `cryptography==42.0.7`
- `daphne==4.1.2`
- `django-data-seed==0.4.1`
- `djangorestframework==3.15.2`
- `redis==5.0.8`
- `websockets==12.0`

## 🗂 Supported Versions

- **Django Versions**:
  - Django 3.2
  - Django 4.x
- **Python Versions**:
  - Python 3.7 - 3.10
- **Databases**:
  - PostgreSQL
  - MySQL
  - SQLite

## 🛡 Security & Permissions

REX ensures robust security by requiring:

- **Token-Based Validation**: Sender and receiver servers must exchange a pre-shared token to initiate communication.
- **Schema Verification**: Ensure both databases have matching schemas before data synchronization begins.
- **Encrypted Data Transfer**: All data, including schema information and individual objects, is encrypted during transmission using the public/private key system.

With REX, the process of migrating data between Django projects is transformed into a seamless, secure, and efficient operation. Whether you're moving data between servers or across different database types, REX takes care of everything—from schema validation to real-time data synchronization—all within the safety of an encrypted connection.

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## 🛠 Support

For any issues or questions, open an issue on the GitHub repository.

## 👤 Author

**Rohith Baggam**

LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/rohith-baggam/)

## 🎨 Frontend Design

The frontend Figma design and development were contributed by:

- [GitHub Profile of Developer 1](https://www.notion.so/c703ebb1b35c482cbde9e0641f7fbf15?pvs=21)
- [Figma Design Link](https://www.notion.so/c703ebb1b35c482cbde9e0641f7fbf15?pvs=21)
