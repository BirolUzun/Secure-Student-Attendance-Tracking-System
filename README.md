<img height="150" src="https://www.emu.edu.tr/static/images/logos/emu-logo-horizontalwhite-en.svg"/>

# Secure Student Attendance Tracking System

This project is CMSE-353 "Security of Software System" Term Project of Fall-2022 by Birol Uzun and Mustafa Evren.

### Description

The Secure Student Attendance Tracking System (SSATS) is a comprehensive solution for tracking and managing student attendance in an educational setting. It has a range of actors with different privileges, including students, teachers, chairs, parents, and system administrators, each of whom can access different features and functions within the system.

Students are only able to view their own attendance records, while teachers can enter and modify attendance for students in their groups. Chairs are able to view attendance records for all students in their department, and parents can view attendance records for their children. System administrators have the highest level of privileges, allowing them to create course-group attendance tables, DES-encrypt data tables, create and update encryption/decryption keys, and introduce new users and grant/revoke privileges.

Data tables in SSATS are kept on the disk and encrypted using DES encryption to ensure the security and confidentiality of the attendance records. Keys for encryption and decryption are created and periodically updated by system administrators to ensure that data remains secure.

Overall, SSATS provides a secure and reliable way to track and manage student attendance, ensuring that all relevant parties are kept informed and up-to-date on attendance patterns.

### Features
- Different actors with different privileges:
  * Student: can view only their own attendance record
  * Teacher: can enter/modify attendance for students in their groups
  * Chair: can view attendance records for all students in their department
  * Parent: can view attendance records for their children
  * System Administrator: can create course-group attendance tables, DES-encrypt data tables, update encryption/decryption keys, introduce new users, and grant/revoke privileges 
- DES-encrypted data tables stored on disk
- System Administrator responsible for creating and updating encryption/decryption keys
- System Administrator can introduce new users and grant/revoke their privileges

### Installation

### Contributors

- [Birol Uzun](https://github.com/Uwillouse) - Team Leader
- [Mustafa Evren]() - Team Member
- [Ali Devecioglu](https://devecy.com) - Team Member (External)