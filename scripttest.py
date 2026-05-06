import pytest
from script import validate_sequence, update_kmer_count, count_kmers_with_context

# tests that a valid DNA sequence should return true
def test_validate_sequence_valid():
    assert validate_sequence("ATGC", 2)

# tests that sequences w invalid chars should return false
def test_validate_sequence_invalid_char():
    assert not validate_sequence("ATXG", 2)

# tests that sequences shorter than k are rejected
def test_validate_sequence_too_short():
    assert not validate_sequence("A", 2)

# test to update an existing k-mer record
def test_update_kmer_count_new():
    data = {}
    result = update_kmer_count(data, "AT", "G")
    assert result["AT"]["count"] == 1
    assert result["AT"]["next_chars"]["G"] == 1

# tests that the first record of a k-mer should initizaluze count = 1
def test_update_kmer_count_existing():
    data = {"AT": {"count": 1, "next_chars": {"G": 1}}}
    result = update_kmer_count(data, "AT", "G")
    assert result["AT"]["count"] == 2
    assert result["AT"]["next_chars"]["G"] == 2

def test_count_kmers_with_context():
    result = count_kmers_with_context("ATG", 2)
    assert result["AT"]["count"] == 1
    assert result["AT"]["next_chars"]["G"] == 1