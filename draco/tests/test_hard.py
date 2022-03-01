from typing import Iterable, Union

from draco import dict_to_facts
from draco.asp_utils import Block
from draco.programs import define, hard, helpers
from draco.run import is_satisfiable, run_clingo


def list_violations(program: Union[str, Iterable[str]]):
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


def no_violations(program: Union[str, Iterable[str]]):
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
    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,text).
    """
        )
        == ["text_mark_without_text_channel"]
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
        )
        == ["text_mark_without_text_channel"]
    )

    # text encoding for a different mark
    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).
    """
        )
        == ["text_mark_without_text_channel"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == ["text_channel_without_text_mark"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).
    """
        )
        == ["bin_and_aggregate"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(mark,root,3).
    """
        )
        == ["no_encodings"]
    )


def test_repeat_channel():
    b = hard.blocks["repeat_channel"]
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

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,m0).
    entity(encoding,m0,e0).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,x).
    """
        )
        == ["repeat_channel"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    attribute((encoding,field),1,temp).
    """
        )
        == ["count_with_field"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,color).
    """
        )
        == ["point_tick_bar_without_x_or_y"]
    )


def test_scale_type_data_type():
    b = hard.blocks["scale_type_data_type"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),temperature,number).
    attribute((field,type),name,string).

    entity(mark,root,1).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).

    entity(scale,root,5).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
    )

    # linear scale/encoding type doesn't support strings
    assert (
        list_violations(
            b.program
            + """
    attribute((field,type),f1,string).

    entity(mark,0,1).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).

    entity(scale,0,5).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
        )
        == ["scale_type_data_type"]
    )

    # previous case with shared scale from root
    assert (
        list_violations(
            b.program
            + """
    attribute((field,type),f1,string).
    entity(view,0,1).

    entity(mark,1,2).
    entity(encoding,2,3).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).

    entity(scale,0,5).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
        )
        == ["scale_type_data_type"]
    )


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
    attribute((encoding,field),2,precipitation).
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
    attribute((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,log).
    """
    )

    # a log scale with only negative numbers
    assert (
        list_violations(
            b.program
            + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,log).
    """
        )
        == ["log_non_positive"]
    )


def test_aggregate_t_valid():
    b = hard.blocks["aggregate_t_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),time,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,min).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((field,type),time,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,max).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,type),time,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,median).
    """
        )
        == ["aggregate_t_valid"]
    )


def test_aggregate_num_valid():
    b = hard.blocks["aggregate_num_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),f1,number).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).
    attribute((encoding,aggregate),3,mean).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,type),f1,string).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).
    attribute((encoding,aggregate),3,sum).
    """
        )
        == ["aggregate_num_valid"]
    )


def test_bin_n_d():
    b = hard.blocks["bin_n_d"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,type),f1,number).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).
    attribute((encoding,binning),3,10).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((field,type),f1,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).
    attribute((encoding,binning),3,10).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,type),f1,string).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,f1).
    attribute((encoding,binning),3,10).
    """
        )
        == ["bin_n_d"]
    )


def test_aggregate_detail():
    b = hard.blocks["aggregate_detail"]
    assert isinstance(b, Block)

    assert (
        list_violations(
            b.program
            + """
    attribute((encoding,channel),2,detail).
    attribute((encoding,aggregate),2,min).
    """
        )
        == ["aggregate_detail"]
    )


def test_count_without_field():
    b = hard.blocks["count_without_field"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,field),2,temp).
    attribute((encoding,aggregate),2,count).
    """
        )
        == ["count_without_field"]
    )


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

    assert (
        list_violations(
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
        )
        == ["count_without_q"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    attribute((scale,channel),4,shape).
    attribute((scale,type),4,categorical).
    """
        )
        == ["categorical_not_color"]
    )


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
    attribute((encoding,field),1,precipitation).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    attribute((encoding,field),1,precipitation).
    """
        )
        == ["size_negative"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,y).
    """
        )
        == ["line_area_without_x_y"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    """
        )
        == ["line_area_without_x_y"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    """
        )
        == ["line_area_without_x_y"]
    )


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

    assert (
        list_violations(
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
        )
        == ["line_area_with_discrete"]
    )


def test_bar_tick_continuous_x_y():
    b = hard.blocks["bar_tick_continuous_x_y"]
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

    # both x and y are continous, and x is binned
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

    # both x and y are continous and binned
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

    assert (
        list_violations(
            b.program
            + """
    entity(view,0,1).

    entity(scale,1,2).
    attribute((scale,channel),2,x).

    entity(scale,0,3).
    attribute((scale,channel),3,x).
    """
        )
        == ["view_scale_conflict"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),0,text).
    entity(encoding,0,1).
    attribute((encoding,channel),1,shape).
    """
        )
        == ["shape_without_point"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),0,bar).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    """
        )
        == ["size_without_point_text"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,0,1).
    entity(encoding,0,2).
    attribute((encoding,channel),1,detail).
    """
        )
        == ["detail_without_agg"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    attribute((mark,type),1,bar).

    entity(scale,0,2).
    attribute((scale,channel),2,y).
    attribute((scale,type),2,log).
    """
        )
        == ["area_bar_with_log"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    attribute((mark,type),1,area).

    entity(scale,0,2).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,log).
    """
        )
        == ["area_bar_with_log"]
    )


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
    assert (
        list_violations(
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
        )
        == ["rect_without_d_d"]
    )

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
    entity(field,root,temperature).
    entity(field,root,date).
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    attribute((encoding,channel),3,y).
    attribute((encoding,field),3,date).
    """
    )

    # same field for x and y
    assert (
        list_violations(
            b.program
            + """
    entity(field,root,temperature).
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(encoding,1,3).

    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    attribute((encoding,channel),3,y).
    attribute((encoding,field),3,temperature).
    """
        )
        == ["same_field_x_and_y"]
    )


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
    assert (
        list_violations(
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
        )
        == ["count_twice"]
    )

    # use count both on x and size
    assert (
        list_violations(
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
        )
        == ["count_twice"]
    )


def test_aggregate_not_all_continuous():
    b = hard.blocks["aggregate_not_all_continuous"]
    assert isinstance(b, Block)

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
    assert (
        list_violations(
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
        )
        == ["aggregate_not_all_continuous"]
    )


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

    assert (
        list_violations(
            b.program
            + """
    attribute((scale,type),4,linear).
    attribute((scale,channel),4,detail).
    """
        )
        == ["detail_not_ordinal"]
    )


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

    # both x and y are continous, and x is binned
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

    # x is continuous and binned, and y is discrete
    assert (
        list_violations(
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
        )
        == ["bar_tick_area_line_without_continuous_x_y"]
    )


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
    attribute((encoding,field),3,2).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,zero),4).

    """
    )

    # x scale start with 0 with string data type
    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).

    entity(field,0,2).
    attribute((field,type),2,string).

    entity(encoding,1,3).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,2).

    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,zero),4).
    """
        )
        == ["zero_d_n"]
    )


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
    attribute((scale,zero),4).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    attribute((scale,zero),5).
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
    attribute((scale,zero),4).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
    )

    # continuous x scale not start with 0
    assert (
        list_violations(
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
        )
        == ["bar_area_without_zero"]
    )

    # continuous y scale not start with 0
    assert (
        list_violations(
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
    attribute((scale,zero),4).

    entity(scale,0,5).
    attribute((scale,channel),5,y).
    attribute((scale,type),5,linear).
    """
        )
        == ["bar_area_without_zero"]
    )
