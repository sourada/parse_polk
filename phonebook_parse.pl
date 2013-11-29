#!/usr/bin/perl
use Switch;

my $crap_line = <>;
my $crap_line = <>;

LINE: while (<>) {
  $last_name="";
  $first_name="";
  $mid_initial="";
  $address="";
  $occupaton="";
  
  next if m/^\\par/;
  if (m/^\\b/) {
    $prev_last_name = "ERROR";
    print STDERR $_;
    next;
  }
  
  s/\\par//;
  s/ +/ /g;
  s/ *$//;
  
  # this needs more rigorous testing like isthe start of next line captial
  if (/-\s*$/) {
    if (!eof()) {
      my $next_line = <>;
      s/\s$/$next_line/;
      redo LINE;
    }
  }
  s/\W*$//;
  
#  s/^\\emdash/$prev_last_name/;
  s/^—/$prev_last_name/;
  
  @line = split(/ /);
  $cols = scalar(@line);
  $col_cnt[$cols]++;
  
  $last_name = shift(@line);

  if (length($line[0]) == 1) {
    $mid_initial = shift(@line);
  } else {
    $first_name = shift(@line) unless scalar(@line) == 0;
  }

  if (length($line[0]) == 1) {
    $mid_initial = shift(@line);
  }
  
  if ((scalar(@line) != 0) && ($line[0] =~ /^\(/ )) {
    while ((scalar(@line) != 0) && ($line[0] !~ /\)$/)) {
      shift(@line);
    }
    shift(@line);
  }
  
  while ((scalar(@line) != 0) && ($line[0] !~ m/[hr][lO\d]\d*|rISC/)) {
    $occupaton .= " ".shift(@line);
  }
  
  $address = &clean_address(shift(@line)) ;
  while ((scalar(@line) != 0)&& (scalar(@line) > 0)) {
    $address .= " " . shift(@line)
  }
  
  if (scalar(@line) > 0) { print STDERR $_;}
  else {printf "%9.9s:%9.9s:%1.1s:%9.9s:%s\n",$last_name,$first_name,$mid_initial,$occupaton,$address;}
#      print $cols . " " . $_;
  $prev_last_name = $last_name unless $last_name == "";
}

#print "\n";
#for $i (0 .. $#col_cnt) {
#  print "$i: $col_cnt[$i]\n";
#}

sub clean_address {
  $_[0] =~ s/l/1/g;
  $_[0] =~ s/O/0/g;
  $_[0];
}

  
