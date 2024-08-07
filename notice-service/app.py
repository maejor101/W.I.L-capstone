from flask import Flask, request, jsonify
import sqlite3
import pdfkit

app = Flask(__name__)

# Replace with your actual database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/create', methods=['POST'])
def create_notice():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO legal_notices (notice_name, language, province, estate_number, curatorship_or_minor_list, person_name, person_address, curator_tutor_name, curator_tutor_address, first_names, surname, address, appointor_terminate_list, from_date, masters_office, advertiser_name, advertiser_address, advertiser_email, date_submitted)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['notice_name'], data['language'], data['province'], data['estate_number'], data['curatorship_or_minor_list'], data['person_name'], data['person_address'], data['curator_tutor_name'], data['curator_tutor_address'], data['first_names'], data['surname'], data['address'], data['appointor_terminate_list'], data['from_date'], data['masters_office'], data['advertiser_name'], data['advertiser_address'], data['advertiser_email'], data['date_submitted']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Legal notice created successfully!"}), 201

@app.route('/visualize', methods=['GET'])
def visualize_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM legal_notices')
    notices = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in notices])

@app.route('/generate_pdf/<int:notice_id>', methods=['GET'])
def generate_pdf(notice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM legal_notices WHERE id = ?', (notice_id,))
    notice = cursor.fetchone()
    conn.close()

    if notice is None:
        return jsonify({"error": "Notice not found"}), 404

    notice_data = dict(notice)

    # Convert the HTML template to PDF
    html_content = f"""
    <h1>Legal Notice</h1>
    <p><strong>Notice Name:</strong> {notice_data['notice_name']}</p>
    <p><strong>Language:</strong> {notice_data['language']}</p>
    <p><strong>Province:</strong> {notice_data['province']}</p>
    <p><strong>Estate Number:</strong> {notice_data['estate_number']}</p>
    <p><strong>Curatorship or Minor List:</strong> {notice_data['curatorship_or_minor_list']}</p>
    <p><strong>Person Name:</strong> {notice_data['person_name']}</p>
    <p><strong>Person Address:</strong> {notice_data['person_address']}</p>
    <p><strong>Curator/Tutor Name:</strong> {notice_data['curator_tutor_name']}</p>
    <p><strong>Curator/Tutor Address:</strong> {notice_data['curator_tutor_address']}</p>
    <p><strong>First Names:</strong> {notice_data['first_names']}</p>
    <p><strong>Surname:</strong> {notice_data['surname']}</p>
    <p><strong>Address:</strong> {notice_data['address']}</p>
    <p><strong>Appointor or Terminate List:</strong> {notice_data['appointor_terminate_list']}</p>
    <p><strong>From Date:</strong> {notice_data['from_date']}</p>
    <p><strong>Masters Office:</strong> {notice_data['masters_office']}</p>
    <p><strong>Advertiser Name:</strong> {notice_data['advertiser_name']}</p>
    <p><strong>Advertiser Address:</strong> {notice_data['advertiser_address']}</p>
    <p><strong>Advertiser Email:</strong> {notice_data['advertiser_email']}</p>
    <p><strong>Date Submitted:</strong> {notice_data['date_submitted']}</p>
    """
    pdf = pdfkit.from_string(html_content, False)
    return send_file(io.BytesIO(pdf), attachment_filename='notice.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
