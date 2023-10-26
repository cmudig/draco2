from typing import Iterable

from draco import dict_to_facts
from draco.asp_utils import Block
from draco.programs import define, hard, helpers
from draco.run import is_satisfiable, run_clingo


def list_violations(program: str | Iterable[str]):
    if not isinstance(program, str):
        program = "\n".join(program)

    try:
        model = next(run_clingo(helpers.program + define.program + program, 1))

        return [
            symbol.arguments[0].name
            for symbol in model.answer_set
            if symbol.name == "violation"
        ]
    except StopIteration:
        return None


def no_violations(program: str | Iterable[str]):
    if not isinstance(program, str):
        program = "\n".join(program)

    return is_satisfiable(
        helpers.program + define.program + program + ":- violation(_)."
    )


def test_list_violations():
    assert list_violations(":- a. :- not a.") is None


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,text).
    """
    )

    # no encoding
    assert list_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    """
    ) == ["text_mark_without_text_channel"]

    assert list_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
    ) == ["text_mark_without_text_channel"]

    # text encoding for a different mark
    assert list_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).
    """
    ) == ["text_mark_without_text_channel"]


def test_text_channel_without_text_mark():
    b = hard.blocks["text_channel_without_text_mark"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
    ) == ["text_channel_without_text_mark"]


def test_bin_and_aggregate():
    b = hard.blocks["bin_and_aggregate"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    entity(encoding,root,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).
    """
    ) == ["bin_and_aggregate"]


def test_no_encodings():
    b = hard.blocks["no_encodings"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(mark,root,3).
    """
    ) == ["no_encodings"]


def test_encoding_repeat_channel():
    b = hard.blocks["encoding_repeat_channel"]
    assert isinstance(b, Block)

    # different channels
    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    entity(encoding,m0,e0).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,y).
    """
    )

    # no channel
    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    """
    )

    # different marks
    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    entity(mark,root,m1).
    entity(encoding,m0,e0).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,x).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,root,m0).
    entity(encoding,m0,e0).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,x).
    """
    ) == ["encoding_repeat_channel"]


def test_scale_repeat_channel():
    b = hard.blocks["scale_repeat_channel"]
    assert isinstance(b, Block)

    # different channels
    assert no_violations(
        b.program
        + """
    entity(scale,v0,s0).
    entity(scale,v0,s1).
    attribute((scale,channel),s0,x).
    attribute((scale,channel),s1,y).
    """
    )

    # different marks
    assert no_violations(
        b.program
        + """
    entity(view,root,v0).
    entity(view,root,v1).
    entity(scale,v0,s0).
    entity(scale,v1,s1).
    attribute((scale,channel),s0,x).
    attribute((scale,channel),s1,x).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(view,root,v0).
    entity(scale,v0,s0).
    entity(scale,v0,s1).
    attribute((scale,channel),s0,x).
    attribute((scale,channel),s1,x).
    """
    ) == ["scale_repeat_channel"]


def test_encoding_channel_without_scale():
    b = hard.blocks["encoding_channel_without_scale"]
    assert isinstance(b, Block)

    # scale and encoding both have x channel
    assert no_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,x).
    """
    )

    # encoding doesn't have y channel, but that's okay
    assert no_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,x).
    entity(scale,v0,s1).
    attribute((scale,channel),s1,y).
    """
    )

    # both have x and y channels
    assert no_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,x).
    entity(scale,v0,s1).
    attribute((scale,channel),s1,y).
    """
    )

    # scale doesn't have x channel
    assert list_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,y).
    """
    ) == ["encoding_channel_without_scale"]


def test_scale_channel_without_encoding():
    b = hard.blocks["scale_channel_without_encoding"]
    assert isinstance(b, Block)

    # scale and encoding both have x channel
    assert no_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,x).
    """
    )

    # scale doesn't have y channel, but that's okay
    assert no_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,x).
    """
    )

    # both have x and y channels
    assert no_violations(
        b.program
        + """
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,x).
    entity(scale,v0,s1).
    attribute((scale,channel),s1,y).
    """
    )

    # encoding doesn't have y channel
    assert list_violations(
        b.program
        + """
    entity(view,root,v0).
    entity(mark,v0,m0).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).

    entity(scale,v0,s0).
    attribute((scale,channel),s0,y).
    """
    ) == ["scale_channel_without_encoding"]


def test_encoding_no_field_and_not_count():
    b = hard.blocks["encoding_no_field_and_not_count"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,field),1,temp).
    attribute((encoding,aggregate),1,mean).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).
    """
    ) == ["encoding_no_field_and_not_count"]


def test_count_with_field():
    b = hard.blocks["count_with_field"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    helper((encoding,field),1,temp).
    """
    ) == ["count_with_field"]


def test_point_tick_bar_without_x_or_y():
    b = hard.blocks["point_tick_bar_without_x_or_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e1,color).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,color).
    """
    ) == ["point_tick_bar_without_x_or_y"]


def test_scale_type_data_type():
    b = hard.blocks["scale_type_data_type"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),f0,number).
    attribute((field,name),f0,temperature).
    attribute((field,type),name,string).

    entity(mark,root,1).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,temperature).

    entity(scale,root,5).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
    )

    # linear scale/encoding type doesn't support strings
    assert list_violations(
        b.program
        + """
    attribute((field,type),f1,string).
    attribute((field,name),f1,temperature).

    entity(mark,0,1).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).

    entity(scale,0,5).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
    ) == ["scale_type_data_type"]

    # previous case with shared scale from root
    assert list_violations(
        b.program
        + """
    attribute((field,type),f1,string).
    attribute((field,name),f1,temperature).
    entity(view,0,1).

    entity(mark,1,2).
    entity(encoding,2,3).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).

    entity(scale,0,5).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
    ) == ["scale_type_data_type"]


def test_log_non_positive():
    b = hard.blocks["log_non_positive"]
    assert isinstance(b, Block)

    # a linear scale with both negative and positive numbers
    assert no_violations(
        b.program
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    # a log scale with only positive numbers
    assert no_violations(
        b.program
        + """
    attribute((field,min),precipitation,10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,log).
    """
    )

    # a log scale with only negative numbers
    assert list_violations(
        b.program
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,log).
    """
    ) == ["log_non_positive"]


def test_aggregate_t_valid():
    b = hard.blocks["aggregate_t_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),time,datetime).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,time).
    attribute((encoding,aggregate),3,min).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((field,type),time,datetime).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,time).
    attribute((encoding,aggregate),3,max).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((field,type),time,datetime).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,time).
    attribute((encoding,aggregate),3,median).
    """
    ) == ["aggregate_t_valid"]


def test_aggregate_num_valid():
    b = hard.blocks["aggregate_num_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),f1,number).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,f1).
    attribute((encoding,aggregate),3,mean).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((field,type),f1,string).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,f1).
    attribute((encoding,aggregate),3,sum).
    """
    ) == ["aggregate_num_valid"]


def test_bin_n_d():
    b = hard.blocks["bin_n_d"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),f1,number).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,f1).
    attribute((encoding,binning),3,10).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((field,type),f1,datetime).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,f1).
    attribute((encoding,binning),3,10).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((field,type),f1,string).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,f1).
    attribute((encoding,binning),3,10).
    """
    ) == ["bin_n_d"]


def test_aggregate_detail():
    b = hard.blocks["aggregate_detail"]
    assert isinstance(b, Block)

    assert list_violations(
        b.program
        + """
    attribute((encoding,channel),2,detail).
    attribute((encoding,aggregate),2,min).
    """
    ) == ["aggregate_detail"]


def test_count_without_q():
    b = hard.blocks["count_without_q"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
    ) == ["count_without_q"]


def test_shape_not_ordinal():
    b = hard.blocks["shape_not_ordinal"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,shape).

    entity(scale,0,3).
    attribute((scale,channel),3,shape).
    attribute((scale,type),3,ordinal).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,shape).

    entity(scale,0,3).
    attribute((scale,channel),3,shape).
    attribute((scale,type),3,categorical).
    """
    ) == ["shape_not_ordinal"]

    # scale on root
    assert list_violations(
        b.program
        + """
    entity(view,root,0).
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,shape).

    entity(scale,root,3).
    attribute((scale,channel),3,shape).
    attribute((scale,type),3,linear).
    """
    ) == ["shape_not_ordinal"]


def test_categorical_not_color():
    b = hard.blocks["categorical_not_color"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((scale,channel),4,color).
    attribute((scale,type),4,categorical).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((scale,channel),4,shape).
    attribute((scale,type),4,categorical).
    """
    ) == ["categorical_not_color"]


def test_size_negative():
    b = hard.blocks["size_negative"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,min),precipitation,0).
    attribute((field,max),precipitation,55).

    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    helper((encoding,field),1,precipitation).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    helper((encoding,field),1,precipitation).
    """
    ) == ["size_negative"]


def test_line_area_without_x_y():
    b = hard.blocks["line_area_without_x_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,y).
    """
    ) == ["line_area_without_x_y"]

    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    """
    ) == ["line_area_without_x_y"]

    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    """
    ) == ["line_area_without_x_y"]


def test_line_area_with_discrete():
    b = hard.blocks["line_area_with_discrete"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,line).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,linear).

    entity(scale,0,3).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,linear).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,line).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,categorical).

    entity(scale,0,3).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,linear).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,line).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,categorical).

    entity(scale,0,3).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,ordinal).
    """
    ) == ["line_area_with_discrete"]


def test_bar_tick_continuous_x_y():
    b = hard.blocks["bar_tick_continuous_x_y"]
    assert isinstance(b, Block)

    # binned histogram
    assert no_violations(
        b.program
        + """
    entity(field,root,0).

    entity(mark,root,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,temperature).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).

    entity(scale,root,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    entity(scale,root,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    # both x and y are continuous, and x is binned
    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    # both x and y are continuous and binned
    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,binning),3,10).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    assert no_violations(
        [b.program]
        + dict_to_facts(
            {
                "mark": [
                    {
                        "type": "tick",
                        "encoding": [
                            {"channel": "x", "field": "temperature"},
                            {"channel": "y", "field": "wind"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear"},
                    {"channel": "y", "type": "categorical"},
                ],
            }
        )
    )

    # multiple views with both linear x and y
    assert list_violations(
        [b.program]
        + dict_to_facts(
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "tick",
                                "encoding": [{"channel": "y", "field": "temperature"}],
                            }
                        ],
                        "scale": [{"channel": "y", "type": "linear"}],
                    },
                    {
                        "mark": [
                            {
                                "type": "bar",
                                "encoding": [
                                    {"channel": "x", "field": "temperature"},
                                    {"channel": "y", "aggregate": "count"},
                                ],
                            }
                        ],
                        "scale": [
                            {"channel": "x", "type": "linear"},
                            {"channel": "y", "type": "linear"},
                        ],
                    },
                ]
            }
        )
    ) == ["bar_tick_continuous_x_y"]

    # multiple views where only y is linear
    assert no_violations(
        [b.program]
        + dict_to_facts(
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "tick",
                                "encoding": [{"channel": "y", "field": "temperature"}],
                            }
                        ]
                    },
                    {
                        "mark": [
                            {
                                "type": "bar",
                                "encoding": [
                                    {"channel": "x", "field": "temperature"},
                                    {"channel": "y", "aggregate": "count"},
                                ],
                            }
                        ],
                        "scale": [{"channel": "x", "type": "ordinal"}],
                    },
                ],
                "scale": [{"channel": "y", "type": "linear"}],
            }
        )
    )

    # multiple views where both x and y are linear
    assert list_violations(
        [b.program]
        + dict_to_facts(
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "tick",
                                "encoding": [{"channel": "y", "field": "temperature"}],
                            }
                        ]
                    },
                    {
                        "mark": [
                            {
                                "type": "bar",
                                "encoding": [
                                    {"channel": "x", "field": "temperature"},
                                    {"channel": "y", "aggregate": "count"},
                                ],
                            }
                        ],
                        "scale": [{"channel": "x", "type": "linear"}],
                    },
                ],
                "scale": [{"channel": "y", "type": "linear"}],
            }
        )
    ) == ["bar_tick_continuous_x_y"]


def test_view_scale_conflict():
    b = hard.blocks["view_scale_conflict"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(view,0,1).

    entity(scale,1,2).
    attribute((scale,channel),2,x).

    entity(scale,0,3).
    attribute((scale,channel),3,y).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(view,0,1).

    entity(scale,1,2).
    attribute((scale,channel),2,x).

    entity(scale,0,3).
    attribute((scale,channel),3,x).
    """
    ) == ["view_scale_conflict"]


def test_shape_without_point():
    b = hard.blocks["shape_without_point"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),0,point).
    entity(encoding,0,1).
    attribute((encoding,channel),1,shape).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((mark,type),0,text).
    entity(encoding,0,1).
    attribute((encoding,channel),1,shape).
    """
    ) == ["shape_without_point"]


def test_size_without_point_text():
    b = hard.blocks["size_without_point_text"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),0,point).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((mark,type),0,text).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((mark,type),0,bar).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    """
    ) == ["size_without_point_text"]


def test_detail_without_agg():
    b = hard.blocks["detail_without_agg"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,0,1).
    entity(encoding,0,2).
    attribute((encoding,channel),1,detail).
    attribute((encoding,aggregate),2,count).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(encoding,0,1).
    entity(encoding,0,2).
    attribute((encoding,channel),1,detail).
    """
    ) == ["detail_without_agg"]


def test_area_bar_with_log():
    b = hard.blocks["area_bar_with_log"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,linear).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,area).

    entity(scale,0,2).
    attribute((scale,channel),2,y).
    attribute((scale,type),2,linear).
    """
    )

    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(scale,0,2).
    attribute((scale,channel),2,y).
    attribute((scale,type),2,log).
    """
    ) == ["area_bar_with_log"]

    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,area).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,log).
    """
    ) == ["area_bar_with_log"]


def test_rect_without_d_d():
    b = hard.blocks["rect_without_d_d"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,rect).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,ordinal).

    entity(scale,0,3).
    attribute((scale,channel),3,y).
    attribute((scale,type),2,ordinal).
    """
    )

    # x is not discrete
    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,rect).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,linear).

    entity(scale,0,3).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,ordinal).
    """
    ) == ["rect_without_d_d"]

    # multiple views where y has log scale
    assert list_violations(
        [b.program]
        + dict_to_facts(
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "tick",
                                "encoding": [{"channel": "y", "field": "temperature"}],
                            }
                        ]
                    },
                    {
                        "mark": [
                            {
                                "type": "rect",
                                "encoding": [
                                    {"channel": "x", "field": "temperature"},
                                    {"channel": "y", "aggregate": "count"},
                                ],
                            }
                        ],
                        "scale": [{"channel": "x", "type": "ordinal"}],
                    },
                ],
                "scale": [{"channel": "y", "type": "log"}],
            }
        )
    ) == ["rect_without_d_d"]


def test_same_field_x_and_y():
    b = hard.blocks["same_field_x_and_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(field,root,f1).
    attribute((field,name),f1,temperature).
    entity(field,root,date).
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    attribute((encoding,channel),3,y).
    helper((encoding,field),3,date).
    """
    )

    # same field for x and y
    assert list_violations(
        b.program
        + """
    entity(field,root,f1).
    attribute((field,name),f1,temperature).
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    attribute((encoding,channel),3,y).
    attribute((encoding,field),3,temperature).
    """
    ) == ["same_field_x_and_y"]


def test_count_twice():
    b = hard.blocks["count_twice"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).

    attribute((encoding,channel),3,y).
    """
    )

    # use count twice but with different marks
    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,3).
    entity(encoding,2,4).

    attribute((encoding,channel),3,x).
    attribute((encoding,aggregate),3,count).

    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,count).
    """
    )

    # use count both on x and y
    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).

    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    """
    ) == ["count_twice"]

    # use count both on x and size
    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).

    attribute((encoding,channel),3,size).
    attribute((encoding,aggregate),3,count).
    """
    ) == ["count_twice"]


def test_aggregate_not_all_continuous():
    b = hard.blocks["aggregate_not_all_continuous"]
    assert isinstance(b, Block)

    # x is binned, thus doesn't need to be aggregated
    assert no_violations(
        b.program
        + """
    entity(field,root,0).

    entity(mark,root,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,temperature).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).

    entity(scale,root,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    entity(scale,root,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    # both x and y are aggregated
    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,mean).

    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,mean).

    entity(scale,root,4).
    attribute((scale,type),4,linear).
    attribute((scale,channel),4,x).
    """
    )

    # x is continuous and aggregated, y is discrete
    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,mean).

    attribute((encoding,channel),3,y).

    entity(scale,root,4).
    attribute((scale,type),4,linear).
    attribute((scale,channel),4,x).

    entity(scale,root,5).
    attribute((scale,type),5,ordinal).
    attribute((scale,channel),5,y).
    """
    )

    # x scale is continuous but not aggregated
    assert list_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).

    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,mean).

    entity(scale,root,4).
    attribute((scale,type),4,linear).
    attribute((scale,channel),4,x).
    """
    ) == ["aggregate_not_all_continuous"]


def test_detail_not_ordinal():
    b = hard.blocks["detail_not_ordinal"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((scale,type),4,ordinal).
    attribute((scale,channel),4,detail).
    """
    )

    assert list_violations(
        b.program
        + """
    attribute((scale,type),4,linear).
    attribute((scale,channel),4,detail).
    """
    ) == ["detail_not_ordinal"]


def test_bar_tick_area_line_without_continuous_x_y():
    b = hard.blocks["bar_tick_area_line_without_continuous_x_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    # both x and y are continuous, and x is binned
    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    # only binned x
    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    ) == ["bar_tick_area_line_without_continuous_x_y"]

    # x is continuous and binned, and y is discrete
    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,ordinal).
    """
    ) == ["bar_tick_area_line_without_continuous_x_y"]


def test_zero_d_n():
    b = hard.blocks["zero_d_n"]
    assert isinstance(b, Block)

    # x scale start with 0 with datetime data type
    assert no_violations(
        b.program
        + """
    entity(mark,0,1).

    entity(field,0,2).
    attribute((field,type),2,number).

    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,2).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,zero),4,true).
    """
    )

    # y scale start with 0 with number data type
    assert no_violations(
        b.program
        + """
    entity(field,root,temperature).
    attribute((field,type),temperature,number).

    entity(field,root,condition).
    attribute((field,type),condition,string).

    entity(mark,root,0).
    attribute((mark,type),0,bar).

    entity(encoding,0,1).
    attribute((encoding,channel),1,x).
    helper((encoding,field),1,condition).

    entity(encoding,0,2).
    attribute((encoding,channel),2,y).
    helper((encoding,field),2,temperature).
    attribute((encoding,aggregate),2,mean).

    entity(scale,root,3).
    attribute((scale,channel),3,x).
    attribute((scale,type),3,ordinal).

    entity(scale,root,4).
    attribute((scale,channel),4,y).
    attribute((scale,type),4,linear).
    attribute((scale,zero),4,true).
    """
    )

    # x scale start with 0 with string data type
    assert list_violations(
        b.program
        + """
    entity(mark,0,1).

    entity(field,0,2).
    attribute((field,type),2,string).

    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    helper((encoding,field),3,2).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,zero),4,true).
    """
    ) == ["zero_d_n"]


def test_bar_area_without_zero():
    b = hard.blocks["bar_area_without_zero"]
    assert isinstance(b, Block)

    # continuous x and y scale start with 0
    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    attribute((scale,zero),4,ture).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    attribute((scale,zero),5,true).
    """
    )

    # binned (not continuous) y scale not start with 0
    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,y).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    attribute((scale,zero),4,true).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    # continuous x scale not start with 0
    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,area).

    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    ) == ["bar_area_without_zero"]

    # continuous y scale not start with 0
    assert list_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    attribute((scale,zero),4,true).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    ) == ["bar_area_without_zero"]


def test_row_no_y():
    b = hard.blocks["row_no_y"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(view,root,0).
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,y).
    entity(facet,0,3).
    attribute((facet,channel),3,row).
    """
    )

    # cannot use row without using y
    assert list_violations(
        p
        + """
    entity(view,root,0).
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(facet,0,3).
    attribute((facet,channel),3,row).
    """
    ) == ["row_no_y"]


def test_col_no_x():
    b = hard.blocks["col_no_x"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(view,root,0).
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(facet,0,3).
    attribute((facet,channel),3,col).
    """
    )

    # cannot use col without using x
    assert list_violations(
        p
        + """
    entity(view,root,0).
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,y).
    entity(facet,0,3).
    attribute((facet,channel),3,col).
    """
    ) == ["col_no_x"]


def test_facet_no_duplicate_field():
    b = hard.blocks["facet_no_duplicate_field"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,field1).
    entity(field,root,1).
    attribute((field,name),1,field2).

    entity(view,root,2).

    entity(facet,2,3).
    attribute((facet,field),3,field1).
    """
    )

    # cannot use the same field twice when faceting
    assert list_violations(
        p
        + """
        entity(field,root,0).
        attribute((field,name),0,field1).
        entity(field,root,1).
        attribute((field,name),1,field2).

        entity(view,root,2).

        entity(facet,2,3).
        attribute((facet,field),3,field1).
        entity(facet,2,4).
        attribute((facet,field),4,field1).
        """
    ) == ["facet_no_duplicate_field"]


def test_facet_no_duplicate_channel_on_same_view():
    b = hard.blocks["facet_no_duplicate_channel_on_same_view"]
    assert isinstance(b, Block)
    p = b.program

    # Single view, single facet
    assert no_violations(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,field1).
    entity(field,root,1).
    attribute((field,name),1,field2).

    entity(view,root,2).

    entity(facet,2,3).
    attribute((facet,channel),3,row).
    """
    )

    # Single view, multi facet (different channels)
    assert no_violations(
        p
        + """
        entity(field,root,0).
        attribute((field,name),0,field1).
        entity(field,root,1).
        attribute((field,name),1,field2).

        entity(view,root,2).

        entity(facet,2,3).
        attribute((facet,channel),3,row).
        entity(facet,2,4).
        attribute((facet,channel),4,col).
        """
    )

    # Multi view, multi facet (same channels)
    assert no_violations(
        p
        + """
        entity(field,root,0).
        attribute((field,name),0,field1).
        entity(field,root,1).
        attribute((field,name),1,field2).

        entity(view,root,2).

        entity(facet,2,3).
        attribute((facet,channel),3,row).

        entity(view,root,4).
        entity(facet,4,5).
        attribute((facet,channel),5,row).
        """
    )

    # Multi view, multi facet (same channels)
    # cannot use the same channel on the same view when faceting
    assert list_violations(
        p
        + """
        entity(field,root,0).
        attribute((field,name),0,field1).
        entity(field,root,1).
        attribute((field,name),1,field2).

        entity(view,root,2).

        entity(facet,2,3).
        attribute((facet,channel),3,row).
        entity(facet,2,4).
        attribute((facet,channel),4,row).
        """
    ) == ["facet_no_duplicate_channel_on_same_view"]


def test_stack_without_bar_area():
    b = hard.blocks["stack_without_bar_area"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(mark,root,2).
    attribute((mark,type),2,bar).

    entity(encoding,2,3).
    attribute((encoding,channel),3,x).

    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,count).
    attribute((encoding,stack),4,zero).
    """
    )

    assert no_violations(
        p
        + """
    entity(mark,root,2).
    attribute((mark,type),2,area).

    entity(encoding,2,3).
    attribute((encoding,channel),3,x).

    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,count).
    attribute((encoding,stack),4,normalize).
    """
    )

    # cannot stack point mark
    assert list_violations(
        p
        + """
    entity(mark,root,2).
    attribute((mark,type),2,point).

    entity(encoding,2,3).
    attribute((encoding,channel),3,x).

    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,count).
    attribute((encoding,stack),4,normalize).
    """
    ) == ["stack_without_bar_area"]


def test_stack_without_summative_agg():
    b = hard.blocks["stack_without_summative_agg"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,count).
    attribute((encoding,stack),4,zero).
    """
    )

    # cannot stack without summative aggregation: no aggregation
    assert list_violations(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,normalize).
    """
    ) == ["stack_without_summative_agg"]

    # cannot stack without summative aggregation: aggregation is not summative
    assert list_violations(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,max).
    attribute((encoding,stack),4,normalize).
    """
    ) == ["stack_without_summative_agg"]


def test_no_stack_with_bar_area_discrete_color():
    b = hard.blocks["no_stack_with_bar_area_discrete_color"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,4).
    attribute((encoding,channel),4,color).
    helper((encoding,field),4,condition).

    entity(scale,0,6).
    attribute((scale,channel),6,y).
    attribute((scale,type),6,linear).
    attribute((scale,zero),6,true).

    entity(scale,0,7).
    attribute((scale,channel),7,color).
    attribute((scale,type),7,categorical).
    """
    )

    # bar/area mark with discrete color, must stack
    assert list_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).

    entity(encoding,1,4).
    attribute((encoding,channel),4,color).
    helper((encoding,field),4,condition).

    entity(scale,0,6).
    attribute((scale,channel),6,y).
    attribute((scale,type),6,linear).
    attribute((scale,zero),6,true).

    entity(scale,0,7).
    attribute((scale,channel),7,color).
    attribute((scale,type),7,categorical).
    """
    ) == ["no_stack_with_bar_area_discrete_color"]


def test_stack_without_discrete_color_or_detail():
    b = hard.blocks["stack_without_discrete_color_or_detail"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,4).
    attribute((encoding,channel),4,color).
    helper((encoding,field),4,condition).

    entity(scale,0,6).
    attribute((scale,channel),6,y).
    attribute((scale,type),6,linear).
    attribute((scale,zero),6,true).

    entity(scale,0,7).
    attribute((scale,channel),7,color).
    attribute((scale,type),7,categorical).
    """
    )

    assert no_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,5).
    attribute((encoding,channel),5,detail).
    helper((encoding,field),5,condition).

    entity(scale,0,7).
    attribute((scale,channel),7,y).
    attribute((scale,type),7,linear).
    attribute((scale,zero),7,true).

    entity(scale,0,9).
    attribute((scale,channel),9,detail).
    attribute((scale,type),9,ordinal).
    """
    )

    # cannot stack without discrete color or detail
    assert list_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,temperature).
    attribute((encoding,binning),2,10).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,4).
    attribute((encoding,channel),4,size).
    helper((encoding,field),4,condition).
    """
    ) == ["stack_without_discrete_color_or_detail"]


def test_stack_without_x_y():
    b = hard.blocks["stack_without_x_y"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,aggregate),4,count).
    attribute((encoding,stack),4,zero).
    """
    )

    # cannot stack without encoding x or y
    assert list_violations(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,color).
    attribute((encoding,stack),4,normalize).
    """
    ) == ["stack_without_x_y"]


def test_stack_discrete():
    b = hard.blocks["stack_discrete"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(scale,0,6).
    attribute((scale,channel),6,y).
    attribute((scale,type),6,linear).
    attribute((scale,zero),6,true).
    """
    )

    # cannot stack on discrete.
    assert list_violations(
        p
        + """
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,binning),3,10).
    attribute((encoding,stack),3,zero).
    """
    ) == ["stack_discrete"]

    assert list_violations(
        p
        + """
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,binning),3,10).
    attribute((encoding,stack),3,zero).

    entity(scale,0,7).
    attribute((scale,channel),7,y).
    attribute((scale,type),7,ordinal).
    """
    ) == ["stack_discrete"]


def test_stack_with_non_positional_non_agg():
    b = hard.blocks["stack_with_non_positional_non_agg"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,4).
    attribute((encoding,channel),4,color).
    attribute((encoding,aggregate),4,count).
    """
    )

    assert no_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,4).
    attribute((encoding,channel),4,color).

    entity(scale,0,8).
    attribute((scale,channel),8,color).
    attribute((scale,type),8,categorical).
    """
    )

    # cannot use non-positional continuous with stack unless it is aggregated.
    assert list_violations(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,aggregate),3,count).
    attribute((encoding,stack),3,zero).

    entity(encoding,1,4).
    attribute((encoding,channel),4,color).

    entity(scale,0,8).
    attribute((scale,channel),8,color).
    attribute((scale,type),8,linear).
    """
    ) == ["stack_with_non_positional_non_agg"]


def test_invalid_bin():
    b = hard.blocks["invalid_bin"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,temperature).
    attribute((encoding,binning),2,30).
    """
    )

    # number of bin cannot be a negative value
    assert list_violations(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    helper((encoding,field),2,temperature).
    attribute((encoding,binning),2,-1).
    """
    ) == ["invalid_bin"]


def test_invalid_num_rows():
    b = hard.blocks["invalid_num_rows"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    attribute(number_rows,root,42).
    """
    )

    # number of rows cannot be 0
    assert list_violations(
        p
        + """
    attribute(number_rows,root,0).
    """
    ) == ["invalid_num_rows"]


def test_invalid_unique():
    b = hard.blocks["invalid_unique"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,unique),date,1461).
    """
    )

    # number of unique value cannot be 0
    assert list_violations(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,unique),date,0).
    """
    ) == ["invalid_unique"]


def test_invalid_extent_non_number():
    b = hard.blocks["invalid_extent_non_number"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,0).
    """
    )

    assert no_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,max),precipitation,55).
    """
    )

    # extent is not allowed for data types other than number
    assert list_violations(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,min),date,0).
    """
    ) == ["invalid_extent_non_number"]

    # extent is not allowed for data types other than number
    assert list_violations(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,max),date,55).
    """
    ) == ["invalid_extent_non_number"]


def test_invalid_non_number_std():
    b = hard.blocks["invalid_non_number_std"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,std),precipitation,6).
    """
    )

    # std is not allowed for data types other than number
    assert list_violations(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,std),date,6).
    """
    ) == ["invalid_non_number_std"]


def test_invalid_std():
    b = hard.blocks["invalid_std"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,std),precipitation,6).
    """
    )

    # std cannot be a negative value
    assert list_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,std),precipitation,-10).
    """
    ) == ["invalid_std"]


def test_invalid_extent_order():
    b = hard.blocks["invalid_extent_order"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,0).
    attribute((field,max),precipitation,55).
    """
    )

    assert no_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,30).
    entity(field,root,precipitation2).
    attribute((field,type),precipitation2,number).
    attribute((field,max),precipitation2,20).
    """
    )

    # min cannot be larger than max
    assert list_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,55).
    attribute((field,max),precipitation,0).
    """
    ) == ["invalid_extent_order"]


def test_invalid_non_string_freq():
    b = hard.blocks["invalid_non_string_freq"]
    assert isinstance(b, Block)
    p = b.program

    assert no_violations(
        p
        + """
    entity(field,root,weather).
    attribute((field,type),weather,string).
    attribute((field,freq),weather,714).
    """
    )

    # freq is not allowed for data types other than string
    assert list_violations(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,freq),precipitation,714).
    """
    ) == ["invalid_non_string_freq"]


def test_enforce_order():
    b = hard.blocks["enforce_order"]
    assert isinstance(b, Block)

    assert list_violations(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,(v,(m,0))).
    entity(mark,v,(v,(m,1))).

    attribute((mark,type),(v,(m,0)),y).
    attribute((mark,type),(v,(m,1)),x).
    """
    ) == ["enforce_order"]

    assert (
        list_violations(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,(v,(m,0))).
    entity(mark,v,(v,(m,1))).

    attribute((mark,type),(v,(m,0)),x).
    attribute((mark,type),(v,(m,1)),y).
    """
        )
        == []
    )
