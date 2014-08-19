/*
 * Italian translation
 * @author Ugo Punzolo <sadraczerouno@gmail.com>
 * @version 2010-09-22
 */
(function ($) {
    if (elFinder && elFinder.prototype.options && elFinder.prototype.options.i18n)
        elFinder.prototype.options.i18n.it = {
            /* errors */
            'Root directory does not exists': 'La cartella principale (root) non esiste',
            'Unable to connect to backend': 'Impossibile stabilire la connessione col server',
            'Access denied': 'Accesso negato',
            'Invalid backend configuration': 'Configurazione con il server non valida',
            'Unknown command': 'Comando sconosciuto',
            'Command not allowed': 'Comando non consentito',
            'Invalid parameters': 'Parametri non corretti',
            'File not found': 'File non trovato',
            'Invalid name': 'Nome non corretto',
            'File or folder with the same name already exists': 'Esiste gi&agrave; una cartella o un file con lo stesso nome',
            'Unable to rename file': 'Impossibile cambiare il nome al file',
            'Unable to create folder': 'Impossibile creare la cartella',
            'Unable to create file': 'Impossibile creare il file',
            'No file to upload': 'Nessun file da caricare',
            'Select at least one file to upload': 'Selezionare almeno un file da caricare',
            'File exceeds the maximum allowed filesize': 'Il file supera le dimensioni consentite',
            'Data exceeds the maximum allowed size': 'I dati superano la grandezza massima consentita',
            'Not allowed file type': 'Tipo di file non consentito',
            'Unable to upload file': 'Impossibile caricare il file',
            'Unable to upload files': 'Impossibile caricare i file',
            'Unable to remove file': 'Impossibile eliminare il file',
            'Unable to save uploaded file': 'No se ha podido guardar el fichero subido',
            'Some files was not uploaded': 'Alcuni file non sono stati caricati',
            'Unable to copy into itself': 'Impossibile copiare all\'interno di se stesso',
            'Unable to move files': 'Impossibile spostare i file',
            'Unable to copy files': 'Impossibile copiare i file',
            'Unable to create file copy': 'Impossibile creare una copia del file',
            'File is not an image': 'Il file non &egrave; un\'immagine',
            'Unable to resize image': 'Impossibile ridimensionare l\'immagine',
            'Unable to write to file': 'Impossibile scrivere il file',
            'Unable to create archive': 'Impossibile creare l\'archivio',
            'Unable to extract files from archive': 'Impossibile estrarre i file dall\'archivio',
            'Unable to open broken link': 'Impossibile aprire il link corrotto',
            'File URL disabled by connector config': 'L\'accesso all\'URL del file &egrave; disabilitato dalla configurazione',
            /* statusbar */
            'items': 'oggetti',
            'selected items': 'oggetti selezionati',
            /* commands/buttons */
            'Back': 'Indietrp',
            'Reload': 'Ricarica',
            'Open': 'Apri',
            'Preview with Quick Look': 'Anteprima veloce',
            'Select file': 'Seleziona file',
            'New folder': 'Nuova cartella',
            'New text file': 'Nuovo file di testo',
            'Upload files': 'Carica file',
            'Copy': 'Copia',
            'Cut': 'Taglia',
            'Paste': 'Incolla',
            'Duplicate': 'Duplica',
            'Remove': 'Elimina',
            'Rename': 'Rinomina',
            'Edit text file': 'Edita il file di testo',
            'View as icons': 'Mostra come icone',
            'View as list': 'Mostra come lista',
            'Resize image': 'Ridimensiona immagine',
            'Create archive': 'Nuovo archivio',
            'Uncompress archive': 'Estrai archivio',
            'Get info': 'Propriet&agrave;',
            'Help': 'Aiuto',
            'Dock/undock filemanager window': 'Separa/unisci la finestra del filemanager',
            /* upload/get info dialogs */
            'Maximum allowed files size': 'Dimensione massima consentita per il file',
            'Add field': 'Aggiungi campo',
            'File info': 'Informazioni file',
            'Folder info': 'Informazioni cartella',
            'Name': 'Nome',
            'Kind': 'Tipo',
            'Size': 'Grandezza',
            'Modified': 'Modificato',
            'Permissions': 'Permessi',
            'Link to': 'Collega a',
            'Dimensions': 'Dimensioni',
            'Confirmation required': 'Richiesta una conferma',
            'Are you sure you want to remove files?<br /> This cannot be undone!': 'Sicuro di voler eliminare il file? <br />Questa azione sar&agrave; irreversibile!',
            /* permissions */
            'read': 'lettura',
            'write': 'scrittura',
            'remove': 'eliminazione',
            /* dates */
            'Jan': 'Gen',
            'Feb': 'Feb',
            'Mar': 'Mar',
            'Apr': 'Apr',
            'May': 'Mag',
            'Jun': 'Giu',
            'Jul': 'Lug',
            'Aug': 'Ago',
            'Sep': 'Set',
            'Oct': 'Ott',
            'Nov': 'Nov',
            'Dec': 'Dic',
            'Today': 'Oggi',
            'Yesterday': 'Ieri',
            /* mimetypes */
            'Unknown': 'Sconosciuto',
            'Folder': 'Cartella',
            'Alias': 'Alias',
            'Broken alias': 'Alias corrotto',
            'Plain text': 'Testo',
            'Postscript document': 'Documento postscript',
            'Application': 'Aplicazione',
            'Microsoft Office document': 'Documento Microsoft Office',
            'Microsoft Word document': 'Documento Microsoft Word',
            'Microsoft Excel document': 'Documento Microsoft Excel',
            'Microsoft Powerpoint presentation': 'Documento Microsoft Powerpoint',
            'Open Office document': 'Documento Open Office',
            'Flash application': 'Aplicazione Flash',
            'XML document': 'Documento XML',
            'Bittorrent file': 'File bittorrent',
            '7z archive': 'Archivo 7z',
            'TAR archive': 'Archivo TAR',
            'GZIP archive': 'Archivo GZIP',
            'BZIP archive': 'Archivo BZIP',
            'ZIP archive': 'Archivo ZIP',
            'RAR archive': 'Archivo RAR',
            'Javascript application': 'Aplicazione Javascript',
            'PHP source': 'Documento PHP',
            'HTML document': 'Documento HTML',
            'Javascript source': 'Documento Javascript',
            'CSS style sheet': 'Documento CSS',
            'C source': 'Documento C',
            'C++ source': 'Documento C++',
            'Unix shell script': 'Script Unix shell',
            'Python source': 'Documento Python',
            'Java source': 'Documento Java',
            'Ruby source': 'Documento Ruby',
            'Perl script': 'Script Perl',
            'BMP image': 'Immagine BMP',
            'JPEG image': 'Immagine JPEG',
            'GIF Image': 'Immagine GIF',
            'PNG Image': 'Immagine PNG',
            'TIFF image': 'Immagine TIFF',
            'TGA image': 'Immagine TGA',
            'Adobe Photoshop image': 'Immagine Adobe Photoshop',
            'MPEG audio': 'Audio MPEG',
            'MIDI audio': 'Audio MIDI',
            'Ogg Vorbis audio': 'Audio Ogg Vorbis',
            'MP4 audio': 'Audio MP4',
            'WAV audio': 'Audio WAV',
            'DV video': 'Video DV',
            'MP4 video': 'Video MP4',
            'MPEG video': 'Video MPEG',
            'AVI video': 'Video AVI',
            'Quicktime video': 'Video Quicktime',
            'WM video': 'Video WM',
            'Flash video': 'Video Flash',
            'Matroska video': 'Video Matroska',
            // 'Shortcuts' : '???????',
            'Select all files': 'Seleziona tutti i file',
            'Copy/Cut/Paste files': 'Copia/Taglia/Incolla file',
            'Open selected file/folder': 'Apri cartella/file selezionato',
            'Open/close QuickLook window': 'Apri/Chiudi finestra anteprima',
            'Remove selected files': 'Elimina file selezionati',
            'Selected files or current directory info': 'Informazioni file elezionati o cartella corrente',
            'Create new directory': 'Nuova cartella',
            'Open upload files form': 'Apri form per caricare file',
            'Select previous file': 'Seleziona file precedente',
            'Select next file': 'Seleziona prossimo file',
            'Return into previous folder': 'Torna alla cartella precedente',
            'Increase/decrease files selection': 'Incrementa/decrementa la selezione dei file',
            'Authors': 'Autori',
            'Sponsors': 'Colaboradores',
            'elFinder: Web file manager': 'elFinder: Web File Manager',
            'Version': 'Versione',
            'Copyright: Studio 42 LTD': 'Copyright: Studio 42',
            'Donate to support project development': 'Dona per supportare lo sviluppo del programma',
            'Javascripts/PHP programming: Dmitry (dio) Levashov, dio@std42.ru': 'Programazione Javascripts/php: Dmitry (dio) Levashov, dio@std42.ru',
            'Python programming, techsupport: Troex Nevelin, troex@fury.scancode.ru': 'Programazione Python, supporto tecnico: Troex Nevelin, troex@fury.scancode.ru',
            'Design: Valentin Razumnih': 'Design: Valentin Razumnyh',
            'Spanish localization': 'Traduzione in italiano: ',
            'Icons': 'Iconos',
            'License: BSD License': 'Licenza: BSD License',
            'elFinder documentation': 'Documentazione elFinder',
            'Simple and usefull Content Management System': 'Un CMS Semplice e funzionale',
            'Support project development and we will place here info about you': 'Sopporta lo sviluppo del software e metteremo qui le informazioni riguardanti te.',
            'Contacts us if you need help integrating elFinder in you products': 'Contattaci se hai bisogno di aiuto per integrare elFinder nei toui prodotti',
            'elFinder support following shortcuts': 'elFinder supporta i seguenti tasti di scelta rapida',
            'helpText': 'elFinder funziona come un comune filemanager per PC. <br />Puoi manipolare i file tramite il pannello principale, il menu o i tasti di scelta rapida. Per spostare i file o le cartelle &egrave; sufficiente trascinarli nella cartella desiderata;	se si preme contemporaneamente anche il tasto Shift i file vengono copiati.'
        };

})(jQuery);
