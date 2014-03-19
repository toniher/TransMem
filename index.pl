#!/usr/bin/env perl

# Automatically enables "strict", "warnings", "utf8" and Perl 5.10 features
use Mojolicious::Lite;
use TransMem;

get '/' => sub {
	my $self = shift;
	$self->render(text => "Hello!");
};

# Route with placeholder
get '/api/seq/:seq' => sub {
	my $self = shift;
	my $seq  = $self->param('seq');
	my $value = process( "ID", $seq );
	
	#my $out;
	#$out->{"result"} = \@outcome;
	#$out->{"seq"} = $seq;
	
	$self->render(text => $value );
};

# Start the Mojolicious command system
app->start;
