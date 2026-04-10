#!/usr/local/bin/perl

umask(000);

$JAVA_HOME = "/export/java";
$JAVA = "/export/java/bin/java";
$JFLAGS = "";
$CLASSPATH = "/export/java/lib/classes.zip:.:/usr/local/etc/httpd/htdocs/tpark/public_html/java/mSQL-JDBC_1.0a4/classes:/usr/local/etc/httpd/htdocs/tpark/public_html/java/classes:.";
$CLASSNAME = "content.trivia.UpdateQuestion";
$CONTENT_LENGTH=35;

@PROPS =("-Dcgi.content_type=$ENV{'CONTENT_TYPE'}",
         "-Dcgi.content_length=$ENV{'CONTENT_LENGTH'}",
         "-Dcgi.request_method=$ENV{'REQUEST_METHOD'}",
         "-Dcgi.mail_directory=\"/usr/local/etc/httpd/htdocs/tpark/public_html/helpsite/mail\"",
         "-Dcgi.templates_directory=\"/usr/local/etc/httpd/htdocs/tpark/public_html/helpsite/templates\"",
         "-Dcgi.query_string=\"$ENV{'QUERY_STRING'}\"");

$CMD = "$JAVA -classpath $CLASSPATH @PROPS $CLASSNAME";

read (STDIN, $buf, $ENV{'CONTENT_LENGTH'});

open (OUT, "|$CMD");
print OUT $buf;
close OUT;    
