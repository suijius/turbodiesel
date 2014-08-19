/*
 * Greek translation
 * @author Panagiotis Skarvelis
 * @version 2010-09-22
 */
(function ($) {
    if (elFinder && elFinder.prototype.options && elFinder.prototype.options.i18n)
        elFinder.prototype.options.i18n.el = {
            /* errors */
            'Root directory does not exists': 'Το Root directory δεν υπάρχει',
            'Unable to connect to backend': 'Αδυναμία σύνδεσης',
            'Access denied': 'Δεν επιτρέπεται η πρόσβαση',
            'Invalid backend configuration': 'Λανθασμένες ρυθμίσεις στον Server',
            'Unknown command': 'Άγνωστη εντολή',
            'Command not allowed': 'Η εντολή δεν επιτρέπεται',
            'Invalid parameters': 'Λανθασμένες παράμετροι',
            'File not found': 'Το αρχείο δεν βρέθηκε',
            'Invalid name': 'Λανθασμένο όνομα',
            'File or folder with the same name already exists': 'Υπάρχει ήδη αρχείο ή  φάκελος με το ίδιο όνομα',
            'Unable to rename file': 'Αδύνατη η μετονομασία του αρχείου',
            'Unable to create folder': 'Αδύνατη η δημιουργία του φακέλου',
            'Unable to create file': 'Αδύνατη η δημιουργία αρχείου',
            'No file to upload': 'Δεν υπάρχει αρχείο για να φορτώσετε',
            'Select at least one file to upload': 'Επιλέξτε τουλάχιστον ένα αρχείο για μεταφόρτωση',
            'File exceeds the maximum allowed filesize': 'Το αρχείο υπερβαίνει το μέγιστο επιτρεπόμενο μέγεθος αρχείου',
            'Not allowed file type': 'Δεν επιτρέπεται ο τύπος του αρχείου',
            'Unable to upload file': 'Αδυναμία φόρτωσης του αρχείου',
            'Unable to upload files': 'Αδυναμία φόρτωσης των αρχείων',
            'Unable to remove file': 'Αδυναμία αφαίρεσης του αρχείου',
            'Unable to save uploaded file': 'Αδυναμία εγγραφής του αρχείου που μεταφορτώθηκε ',
            'Some files was not uploaded': 'Ορισμένα αρχεία δεν μεταφορτώθηκαν',
            'Unable to copy into itself': 'Δεν μπορώ να κάνω αντίγραφο με το ίδιο όνομα',
            'Unable to move files': 'Αδυναμία μετακίνησης των αρχείων',
            'Unable to copy files': 'Αδυναμία αντιγραφής των αρχείων',
            'Unable to create file copy': 'Αδύνατη η δημιουργία του αρχείου αντιγράφου',
            'File is not an image': 'Το αρχείο δεν είναι αρχείο εικόνας',
            'Unable to resize image': 'Αδύνατη η αλλαγής μεγέθους της εικόνας',
            'Unable to write to file': 'Αδύνατη η εγγραφή στο αρχείο',
            'Unable to create archive': 'Αδύνατη η δημιουργία του συμπιεσμένου αρχείου',
            'Unable to extract files from archive': 'Αδύνατη η εξαγωγή των αρχείων από το συμπιεσμένο αρχείο',
            'Unable to open broken link': 'Αδυναμία στο άνοιγμα λόγο σπασμένης σύνδεσης (file link)',
            'File URL disabled by connector config': 'Τα URL αρχείου είναι καταργημένα στις ρυθμίσεις του server',
            /* statusbar */
            'items': 'αντικείμενα',
            'selected items': 'επιλεγμένα αντικείμενα',
            /* commands/buttons */
            'Back': 'Πίσω',
            'Reload': 'Ανανέωση',
            'Open': 'Άνοιγμα',
            'Preview with Quick Look': 'Προεπισκόπηση Quick Look',
            'Select file': 'Επιλέξτε αρχείο',
            'New folder': 'Νέος φάκελος',
            'New text file': 'Νέο αρχείο κειμένου',
            'Upload files': 'Μεταφόρτωση αρχείων',
            'Copy': 'Αντιγραφή',
            'Cut': 'Αποκοπή',
            'Paste': 'Επικόλληση',
            'Duplicate': 'Αντίγραφο',
            'Remove': 'Αφαίρεση',
            'Rename': 'Μετονομασία',
            'Edit text file': 'Επεξεργασία αρχείου κειμένου',
            'View as icons': 'Προβολή ως εικονίδια',
            'View as list': 'Προβολή λίστας',
            'Resize image': 'Αλλαγή μεγέθους της εικόνας',
            'Create archive': 'Δημιουργία συμπιεσμένου',
            'Uncompress archive': 'Αποσυμπίεση',
            'Get info': 'Πληροφορίες',
            'Help': 'Βοήθεια',
            'Dock/undock filemanager window': 'Ελεύθερο/Αγκιστρωμένο παράθυρο',
            /* upload/get info dialogs */
            'Maximum allowed files size': 'Μέγιστο επιτρεπόμενο μέγεθος αρχείων',
            'Add field': 'Προσθήκη πεδίου',
            'File info': 'Πληροφορίες αρχείου',
            'Folder info': 'Πληροφορίες φακέλου',
            'Name': 'Όνομα',
            'Kind': 'Είδος',
            'Size': 'Μέγεθος',
            'Modified': 'Τροποποιημένο',
            'Permissions': 'Άδειες',
            'Link to': 'Σύνδεσμος σε',
            'Dimensions': 'Διαστάσεις',
            'Confirmation required': 'Απαιτείται επιβεβαίωση',
            'Are you sure you want to remove files?<br /> This cannot be undone!': 'Θέλετε σίγουρα να καταργήσετε τα αρχεία; <br /> Η εντολή είναι μη αναστρέψιμη!',
            /* permissions */
            'read': 'Ανάγνωση',
            'write': 'Εγγραφή',
            'remove': 'Απομάκρυνση',
            /* dates */
            'Jan': 'Ιανουάριος',
            'Feb': 'Φεβρουάριος',
            'Mar': 'Μάρτιος',
            'Apr': 'Απρίλιος',
            'May': 'Μαιος',
            'Jun': 'Ιούνιος',
            'Jul': 'Ιούλιος',
            'Aug': 'Άυγουστος',
            'Sep': 'Σεπτέμβριος',
            'Oct': 'Οκτώβριος',
            'Nov': 'Νοέμβριος',
            'Dec': 'Δεκέμβριος',
            'Today': 'Σήμερα',
            'Yesterday': 'Χθές',
            /* mimetypes */
            'Unknown': 'Άγνωστος',
            'Folder': 'Φάκελος',
            'Alias': 'Σύνδεσμος',
            'Broken alias': 'Σπασμένος Σύνδεσμος',
            'Plain text': 'Απλό κείμενο',
            'Postscript document': 'Αρχείο postscript',
            'Application': 'Εφαρμογή',
            'Microsoft Office document': 'Αρχείο Microsoft Office',
            'Microsoft Word document': 'Αρχείο Microsoft Word',
            'Microsoft Excel document': 'Αρχείο Microsoft Excel',
            'Microsoft Powerpoint presentation': 'Παρουσίαση Microsoft Powerpoint',
            'Open Office document': 'Αρχείο Open Office',
            'Flash application': 'Εφαρμογή Flash',
            'XML document': 'Αρχείο XML',
            'Bittorrent file': 'Αρχείο Bittorrent',
            '7z archive': 'Συμπιεσμένο αρχείο 7z',
            'TAR archive': 'Συμπιεσμένο αρχείο TAR',
            'GZIP archive': 'Συμπιεσμένο αρχείο GZIP',
            'BZIP archive': 'Συμπιεσμένο αρχείο BZIP',
            'ZIP archive': 'Συμπιεσμένο αρχείο ZIP',
            'RAR archive': 'Συμπιεσμένο αρχείο RAR',
            'Javascript application': 'Εφαρμογή Javascript',
            'PHP source': 'Κώδικας PHP',
            'HTML document': 'Αρχείο HTML',
            'Javascript source': 'Κώδικας Javascript',
            'CSS style sheet': 'Φύλλο στυλ CSS',
            'C source': 'Κώδικας C',
            'C++ source': 'Κώδικας C++',
            'Unix shell script': 'Εφαρμογή κελύφους Unix',
            'Python source': 'Κώδικας Python',
            'Java source': 'Κώδικας Java',
            'Ruby source': 'Κώδικας Ruby',
            'Perl script': 'Εφαρμογή Perl',
            'BMP image': 'Εικόνα BMP',
            'JPEG image': 'Εικόνα JPEG',
            'GIF Image': 'Εικόνα GIF',
            'PNG Image': 'Εικόνα PNG',
            'TIFF image': 'Εικόνα TIFF',
            'TGA image': 'Εικόνα TGA',
            'Adobe Photoshop image': 'Εικόνα Adobe Photoshop',
            'MPEG audio': 'Ήχος MPEG',
            'MIDI audio': 'Ήχος MIDI',
            'Ogg Vorbis audio': 'Ήχος Ogg Vorbis',
            'MP4 audio': 'Ήχος MP4',
            'WAV audio': 'Ήχος WAV',
            'DV video': 'Βίντεο DV',
            'MP4 video': 'Βίντεο MP4',
            'MPEG video': 'Βίντεο MPEG',
            'AVI video': 'Βίντεο AVI',
            'Quicktime video': 'Βίντεο Quicktime',
            'WM video': 'Βίντεο WM',
            'Flash video': 'Βίντεο Flash',
            'Matroska video': 'Βίντεο Matroska',
            // 'Shortcuts' : 'Клавиши',
            'Select all files': 'Επιλέξτε όλα τα αρχεία',
            'Copy/Cut/Paste files': 'Αντιγραφή / Αποκοπή / Επικόλληση αρχείων',
            'Open selected file/folder': 'Άνοιγμα επιλεγμένου αρχείου / φακέλου',
            'Open/close QuickLook window': 'Άνοιγμα/κλείσιμο παραθύρου QuickLook  ',
            'Remove selected files': 'Αφαιρέστε τα επιλεγμένα αρχεία',
            'Selected files or current directory info': 'Πληροφορίες του καταλόγου ή των επιλεγμένων αρχείων',
            'Create new directory': 'Δημιουργία νέου καταλόγου',
            'Open upload files form': 'Ανοίξετε την φόρμα μεταφόρτωσης αρχείων',
            'Select previous file': 'Επιλογή προηγούμενου αρχείου',
            'Select next file': 'Επιλογή επόμενου αρχείου',
            'Return into previous folder': 'Επιστροφή στον προηγούμενο φάκελο',
            'Increase/decrease files selection': 'Αύξηση / μείωση της επιλογής αρχείων',
            'Authors': 'Συγγραφείς',
            'Sponsors': 'Χορηγοί',
            'elFinder: Web file manager': 'elFinder: Web διαχειριστής αρχείων',
            'Έκδοση': 'Версія',
            'Copyright: Studio 42 LTD': 'Πνευματική ιδιοκτησία: Studio 42 LTD',
            'Donate to support project development': 'Κάντε δωρεά για την υποστήριξη της ανάπτυξης του έργου',
            'Javascripts/PHP programming: Dmitry (dio) Levashov, dio@std42.ru': 'Προγραμματισμός Javascript/PHP : Dmitry (dio) Levashov, dio@std42.ru',
            'Python programming, techsupport: Troex Nevelin, troex@fury.scancode.ru': 'Προγραμματισμός Python , Τεχνική υποστήριξη: Troex Nevelin, troex@fury.scancode.ru',
            'Design: Valentin Razumnih': 'Σχεδιασμός: Razumnih Valentin',
            'Spanish localization': 'Ισπανική μετάφραση',
            'Icons': 'Εικονίδια',
            'License: BSD License': 'Άδεια: BSD License',
            'elFinder documentation': 'elFinder Τεκμηρίωση',
            'Simple and usefull Content Management System': 'Απλό και χρήσιμο Σύστημα Διαχείρισης Περιεχομένου',
            'Support project development and we will place here info about you': 'Υποστηρίξτε την ανάπτυξη του έργου και θα βάλουμε εδώ πληροφορίες για εσάς',
            'Contacts us if you need help integrating elFinder in you products': 'Ελάτε σε επαφή μαζί μας αν χρειάζεστε βοήθεια για την ενσωμάτωση του elFinder σε δικά σας προϊόντα',
            'helpText': 'Το elFinder λειτουργεί παρόμοια με τον διαχειριστή αρχείων του υπολογιστή σας.<br /> Η Διαχείριση των αρχείων γίνετε χρησιμοποιώντας τα εικονίδια στην γραμμή εργαλείων , μέσο μενού που εμφανίζετε με το δεξί πλήκτρο του ποντικιού  ή μέσο  συντομεύσεων πληκτρολογίου.Για να μετακινήσετε  αρχεία / φακέλους, απλά τα επιλέγετε και τα μετακινείτε στο επιθυμητό εικονίδιο φακέλου.Αν κρατάτε πατημένο το πλήκτρο Shift τα αρχεία θα αντιγραφούν.<br/> <br/> Το ElFinder υποστηρίζει τις παρακάτω συντομεύσεις πληκτρολογίου:'

        };

})(jQuery);
