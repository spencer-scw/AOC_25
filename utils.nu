#!/usr/bin/env nu

export def bootstrap [day: int] {
  mkdir $"day($day)"
  get input $day | save $"day($day)/input.txt"
  cd $"day($day)"
  touch part1.py part2.py test.txt
}

def "get input" [day: int] {
  open aoc-session.yml |
  http get $"($in.base-url)day/($day)/input" --headers ($in | select cookie)
}

export def "run day" [day: int part?: int] {
    cd $"day($day)"
    if $part != null {
      try { python3 $"part($part).py" } catch { |err| $err.msg }
    } else {
      glob $"part*.py" | sort | each {|f| try { python3 $f } catch { |err| $err.msg }}
    }
}

export def "iterate on day" [day: int part: int] {
    let path = $"day($day)"
    watch $path { |op| if $op == "Create" {run day $day $part }}
}
