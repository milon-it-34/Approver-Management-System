def email_template(full_name, teacher_name, subject, description, student_no, date, email, batch):
    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
    <body>
        <p>
            Dear <strong style="color: rgb(53, 53, 97);">{teacher_name} </strong>Sir,
            <br><br>
            <p>
              I am writing to request a discussion regarding my project/thesis. Below are the details:
          </p>      
        <ul>
            <li><strong style="color: chocolate;">Subject: </strong>{subject}</li>
            <li><strong style="color: darkgreen;">Description: </strong>{description}</li>
            <li><strong style="color: darkred;">Date: </strong> <span style="background-color: rgb(201, 193, 193);">{date}</span></li>
        </ul>
        <p>
            It would be greatly appreciated if we could schedule a meeting or discussion regarding this project/thesis on or around the provided date.
        </p>
        <p>
            Thank you for your consideration.
            <br><br>
            Sincerely,
            <br>
            <br>
            <strong>{full_name}</strong>
            <br>
            <span><strong style="color: rgb(95, 89, 89);">Email: </strong> {email}</span>
            <br>
            <span><strong style="color: rgb(95, 89, 89);">Batch: </strong> {batch}</span>
            <br>
            <span><strong style="color: rgb(95, 89, 89);">Student ID: </strong>{student_no}</span>
            <br>
            <b>Department of Information and Communication Technology<br>
            @ Mawlana Bhashani Science and Technology University</b>
        </p>
    </body>
    </html>
    """
    return html_message
